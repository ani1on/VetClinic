from pydantic import Field, BaseModel
from typing import Optional
from datetime import datetime
from . import ORMModel

class ReviewCreateRequest(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None

class ReviewModerateRequest(BaseModel):
    status: str = Field(..., pattern='^(approved|rejected)$')

class ReviewResponse(ORMModel):
    id: int
    user_id: int
    rating: int
    comment: Optional[str]
    status: str
    created_at: datetime
    # если нужно – можно добавить user_name
    # user_name: Optional[str] = None

class ReviewListResponse(ORMModel):
    total: int
    reviews: list[ReviewResponse]