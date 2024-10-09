import logging
from fastapi import APIRouter, Response, Query, HTTPException
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
        status_code, product_list = crawl_products(page_limit)
        if status_code == 200:
            return ProductResponse(
                product_list=[ProductDetails(
                    name=p.get('name'),  # Use .get() to safely access dictionary keys
                    app_name=p.get('app_name'),
                    buy_price=p.get('buy_price'),
                    sell_offers=p.get('sell_offers'),
                    sell_price=p.get('sell_price'),
                    marketable=p.get('marketable')
                ) for p in product_list])
        elif status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Products not found"
            )
        elif status_code in (403, 429):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Crawler is getting blocked by the source."
            )
        elif status_code == 500:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error while fetching products"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid request"
            )
    except Exception as message:
        logger.error(f"Error: {str(message)}")
        return ProductResponse(error=str(message))
