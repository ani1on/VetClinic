from pydantic import Field, BaseModel
from typing import Optional
from . import ORMModel

class ProductCreateRequest(BaseModel):
    name: str = Field(..., max_length=200)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    category: Optional[str] = None
    stock_quantity: int = Field(default=0, ge=0)
    image_url: Optional[str] = None

class ProductUpdateRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    stock_quantity: Optional[int] = None
    is_available: Optional[bool] = None
    image_url: Optional[str] = None

class ProductStockUpdate(BaseModel):
    quantity: Optional[int] = None
    is_available: Optional[bool] = None

class ProductResponse(ORMModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    category: Optional[str]
    stock_quantity: int
    is_available: bool
    image_url: Optional[str]

class ProductListResponse(ORMModel):
    total: int
    products: list[ProductResponse]