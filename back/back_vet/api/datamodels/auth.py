from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from . import ORMModel

# ---- Запросы ----
class RegisterRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    phone: str = Field(..., pattern=r'^\+?\d{10,15}$')
    email: Optional[EmailStr] = None
    password: str = Field(..., min_length=6)
    role: Optional[str] = "client"

class LoginRequest(BaseModel):
    login: str = Field(..., description="Email или телефон")
    password: str

class RefreshRequest(BaseModel):
    refresh_token: str

class ForgotPasswordRequest(BaseModel):
    email: Optional[str] = None
    phone: Optional[str] = None

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(..., min_length=6)

# ---- Ответы ----
class TokenResponse(ORMModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class UserProfileResponse(ORMModel):   # базовая информация о пользователе в ответе авторизации
    id: int
    name: str
    phone: str
    email: Optional[str]
    role: str
    created_at: datetime

class AuthResponse(TokenResponse):
    user: UserProfileResponse