import pytest
from app.core.services.product_extractor import crawl_products

@pytest.mark.parametrize("page_limit, expected_count", [
    (0, 0),        # Testing with 0 pages
    (3, 30),       # Testing with 3 pages
    (50, 500),     # Testing with 50 pages
])
def test_crawl_products(page_limit, expected_count):
    product_list = crawl_products(page_limit=page_limit)
    assert len(product_list) == expected_count
