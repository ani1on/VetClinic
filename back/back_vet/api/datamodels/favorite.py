from pydantic import Field
from datetime import datetime
from . import ORMModel

class FavoriteCreateRequest(BaseModel):
    entity_type: str = Field(..., regex='^(product|service|doctor)$')
    entity_id: int

class FavoriteResponse(ORMModel):
    id: int
    user_id: int
    entity_type: str
    entity_id: int
    created_at: datetime