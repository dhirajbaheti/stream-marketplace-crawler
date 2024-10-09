import logging
import requests
from app.config.logging import setup_logging
from typing import List
from app.core.models.product import ProductDetails

setup_logging()
logger = logging.getLogger(__name__)

def get_proxy():
    """
    This is a helper function to get the proxy for each request.
    Currently it uses dummy values which needs to be replaced with the actual for production environment.
    """
    proxy_host = "xxxxxx.com"
    proxy_port = "19888"
    proxies = {"https": "http://{}:{}/".format(proxy_host, proxy_port),
               "http": "http://{}:{}/".format(proxy_host, proxy_port)}

    return proxies

def parse_products(response):
    """
    Parse the response from the server and return list of products.
    """
    products = []
    data = response.json()
    for item in data["results"]:
        product = {
            "name": item["name"],
            "app_name": item["app_name"],
            "buy_price": item["sale_price_text"],
            "sell_offers": item["sell_listings"],
            "sell_price": item["sell_price_text"],
            "marketable": item["asset_description"]["marketable"],
        }
        products.append(product)

    return products

def crawl_products(page_limit: int):
    """
    This function is used to crawl the products from streamcommunity.com and return list of products.
    Input: page_limit(int)
    Output: status, product_list
    """
    status = None
    response = None
    product_list = []
    pagesize = 10
    raw_url = "https://steamcommunity.com/market/search/render/?norender=1&query=&start={start}&count=10&search_descriptions=0&sort_column=popular&sort_dir=desc"
    for page in range(page_limit):
        for _ in range(3):
            try:
                logger.info(f"Crawling products from page:{page + 1}")
                url = raw_url.format(start=page * pagesize)
                headers = {
                    'Accept': 'text/javascript, text/html, application/xml, text/xml, */*',
                    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
                    'Connection': 'keep-alive',
                    'Referer': 'https://steamcommunity.com/market/search?q=',
                    'Sec-Fetch-Dest': 'empty',
                    'Sec-Fetch-Mode': 'cors',
                    'Sec-Fetch-Site': 'same-origin',
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
                    'X-Prototype-Version': '1.7',
                    'X-Requested-With': 'XMLHttpRequest',
                    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"macOS"'
                }
                response = requests.get(url, headers=headers, proxies=get_proxy())
                status = response.status_code
                response.raise_for_status()
                product_list.extend(parse_products(response))
                break
            except Exception as e:
                if response.status_code in (403, 429):
                    logger.error(f"Crawler is being blocked. {e}.")
                    break
                logger.warning(f"Exception occurred while crawling products. {e}. Retrying")

        if response.status_code in (403, 429):
            break

    if status == 200:
        logger.info(f"Extracted {len(product_list)} products from {page_limit} pages.")

    return status, product_list
