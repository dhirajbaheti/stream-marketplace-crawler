import logging
from fastapi import APIRouter, Response, Query
from starlette import status
from typing import Optional, List
from app.config.logging import setup_logging
from app.core.models.product import ProductDetails, ProductResponse
from app.core.services.product_extractor import crawl_products

router = APIRouter()

setup_logging()
logger = logging.getLogger(__name__)

@router.get(
    "/get_products", response_model=ProductResponse, status_code=status.HTTP_200_OK
)
def get_products(page_limit: Optional[int] = Query(None, example=5)):
    logger.info(f"Request: page_limit: {page_limit}")

    try:
        product_list = crawl_products(page_limit)

        # Assuming product_list is a list of dictionaries
        return ProductResponse(
            product_list=[ProductDetails(
                name=p.get('name'),  # Use .get() to safely access dictionary keys
                app_name=p.get('app_name'),
                buy_price=p.get('buy_price'),
                sell_offers=p.get('sell_offers'),
                sell_price=p.get('sell_price'),
                marketable=p.get('marketable')
            ) for p in product_list])
    except Exception as message:
        logger.error(f"Error: {str(message)}")
        return ProductResponse(product_list=[])