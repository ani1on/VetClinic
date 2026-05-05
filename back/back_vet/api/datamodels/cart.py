from pydantic import Field, validator, BaseModel
from typing import Optional
from . import ORMModel
from .product import ProductResponse

class CartItemCreateRequest(BaseModel):
    product_id: int
    quantity: int = Field(default=1, gt=0)

class CartItemUpdateRequest(BaseModel):
    quantity: int = Field(..., gt=0)

class CartItemResponse(ORMModel):
    id: int
    product_id: int
    quantity: int
    product: Optional[ProductResponse] = None   # подгружаем товар при запросе корзины

class CartResponse(ORMModel):
    items: list[CartItemResponse]
    total_price: float = 0.0   # можно вычислить на бэке