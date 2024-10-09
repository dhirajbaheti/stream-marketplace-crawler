from typing import Optional, List
from pydantic import Field, BaseModel


class ProductRequest(BaseModel):
    page_limit: Optional[int] = Field(default=5, json_schema_extra={"example": 10})

class ProductDetails(BaseModel):
    name: str = Field(json_schema_extra={"example": "Counter-Strike 2"})
    app_name: str = Field()
    buy_price: str = Field()
    sell_price: str = Field()
    sell_offers: int = Field()
    marketable: bool = Field()

class ProductResponse(BaseModel):
    product_list: List[ProductDetails]
