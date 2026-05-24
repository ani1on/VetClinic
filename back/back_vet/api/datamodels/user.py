from pydantic import Field, BaseModel
from typing import Optional, List
from datetime import datetime
from . import ORMModel
from .pet import PetResponse


class UserUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    phone: Optional[str] = Field(None, pattern=r'^\+?\d{10,15}$')
    email: Optional[str] = None


class UserDetailResponse(ORMModel):
    id: int
    name: str
    phone: str
    email: Optional[str]
    role: str
    created_at: datetime


class UserProfileResponse(ORMModel):
    id: int
    name: str
    phone: str
    email: Optional[str]
    pets: Optional[List[PetResponse]] = []


class UserListResponse(ORMModel):
    total: int
    users: List[UserDetailResponse]


class UserRoleUpdateRequest(BaseModel):
    role: str = Field(..., pattern="^(client|admin)$", description="Роль: client или admin")