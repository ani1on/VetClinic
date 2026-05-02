from pydantic import Field
from typing import Optional
from datetime import datetime
from . import ORMModel

class NewsCreateRequest(BaseModel):
    title: str = Field(..., max_length=200)
    content: Optional[str] = None
    image_url: Optional[str] = None
    is_published: bool = True

class NewsUpdateRequest(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    image_url: Optional[str] = None
    is_published: Optional[bool] = None

class NewsResponse(ORMModel):
    id: int
    title: str
    content: Optional[str]
    image_url: Optional[str]
    is_published: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

class NewsListResponse(ORMModel):
    total: int
    news: list[NewsResponse]