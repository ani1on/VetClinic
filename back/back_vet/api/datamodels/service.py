from pydantic import Field, BaseModel
from typing import Optional
from . import ORMModel

class ServiceCreateRequest(BaseModel):
    name: str = Field(..., max_length=200)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    duration_minutes: int = Field(default=30, gt=0)
    category: Optional[str] = None

class ServiceUpdateRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    duration_minutes: Optional[int] = None
    category: Optional[str] = None
    is_active: Optional[bool] = None

class ServiceResponse(ORMModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    duration_minutes: int
    category: Optional[str]
    is_active: bool