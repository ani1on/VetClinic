from pydantic import Field,BaseModel
from typing import Optional, List
from datetime import datetime
from . import ORMModel
from .product import ProductResponse

class OrderCreateRequest(BaseModel):
    notes: Optional[str] = None   # заказ формируется из корзины, здесь только дополнительные поля

class OrderStatusUpdate(BaseModel):
    status: str = Field(..., pattern='^(pending|confirmed|shipped|delivered|canceled)$')

class OrderItemResponse(ORMModel):
    id: int
    product_id: int
    quantity: int
    price_per_unit: float
    product: Optional[ProductResponse] = None

class OrderResponse(ORMModel):
    id: int
    user_id: int
    status: str
    total_amount: float
    created_at: datetime
    notes: Optional[str]
    items: List[OrderItemResponse] = []

class OrderListResponse(ORMModel):
    total: int
    orders: List[OrderResponse]