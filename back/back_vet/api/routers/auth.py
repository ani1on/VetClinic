from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from back.back_vet.database.core import get_db
from ...database.methods import user_methods
from ..datamodels.auth import (
    RegisterRequest,
    LoginRequest,
    RefreshRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    TokenResponse,
    AuthResponse,
    UserProfileResponse,
)
from ..dependencies import get_current_user   # будет определен ниже (или в отдельном файле)
from ...database.models import User

# Конфигурация безопасности
SECRET_KEY = "your-secret-key-keep-it-secret"   # Лучше вынести в .env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

router = APIRouter(prefix="/api/auth", tags=["auth"])

# ---------- Вспомогательные функции ----------
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict):
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = data.copy()
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_user_by_token(db: Session, token: str) -> Optional[User]:
    """Получить пользователя по JWT (для зависимостей)."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            return None
    except JWTError:
        return None
    return user_methods.get_user_by_id(db, user_id)

# ---------- Эндпоинты ----------
@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    # Проверяем, не занят ли телефон или email
    if request.email and user_methods.find_user_by_email(db, request.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    if user_methods.find_user_by_phone(db, request.phone):
        raise HTTPException(status_code=400, detail="Phone already registered")

    # Хешируем пароль и создаём пользователя
    hashed_password = pwd_context.hash(request.password)
    user = user_methods.create_user(
        db,
        name=request.name,
        phone=request.phone,
        email=request.email,
        password_hash=hashed_password,
        role=request.role or "client"
    )

    # Генерируем токены
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    # Сохраняем refresh-токен в БД
    user_methods.save_refresh_token(
        db,
        user_id=user.id,
        token=refresh_token,
        expires_at=datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )

    return AuthResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserProfileResponse.from_orm(user)
    )

@router.post("/login", response_model=AuthResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    # Ищем пользователя по email или телефону
    user = None
    if "@" in request.login:
        user = user_methods.find_user_by_email(db, request.login)
    else:
        user = user_methods.find_user_by_phone(db, request.login)

    if not user or not pwd_context.verify(request.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Генерируем токены
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    # Сохраняем refresh
    user_methods.save_refresh_token(
        db,
        user_id=user.id,
        token=refresh_token,
        expires_at=datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )

    return AuthResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserProfileResponse.from_orm(user)
    )

@router.post("/refresh", response_model=TokenResponse)
def refresh_token(request: RefreshRequest, db: Session = Depends(get_db)):
    # Проверяем refresh-токен в БД
    stored_token = user_methods.validate_refresh_token(db, request.refresh_token)
    if not stored_token:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    # Получаем пользователя (можно из stored_token.user_id)
    user = user_methods.get_user_by_id(db, stored_token.user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    # Отзываем старый refresh
    user_methods.revoke_refresh_token(db, request.refresh_token)

    # Генерируем новую пару
    new_access = create_access_token({"sub": str(user.id)})
    new_refresh = create_refresh_token({"sub": str(user.id)})

    user_methods.save_refresh_token(
        db,
        user_id=user.id,
        token=new_refresh,
        expires_at=datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )

    return TokenResponse(access_token=new_access, refresh_token=new_refresh)

@router.post("/logout")
def logout(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # Отзываем refresh-токен (не access!). Access токен короткоживущий.
    # Здесь мы можем потребовать refresh_token в теле, но для простоты просто заглушим,
    # либо примем refresh из тела запроса. Согласно спецификации, у нас есть метод logout,
    # который должен инвалидировать refresh. Добавим дополнительный параметр refresh_token.
    # Для простоты примера: клиент передаёт refresh_token в теле (не в заголовке).
    # Но по спецификации нет параметров. Можно сделать так, чтобы logout получал refresh_token из тела.
    pass
    # Реальная реализация: принимаем refresh_token в теле и отзываем.
    # user_methods.revoke_refresh_token(db, refresh_token)
    # return {"message": "Logged out"}

@router.post("/logout", description="Revoke refresh token")   # альтернативно передадим refresh_token
async def logout(request: RefreshRequest, db: Session = Depends(get_db)):
    user_methods.revoke_refresh_token(db, request.refresh_token)
    return {"message": "Successfully logged out"}

@router.post("/forgot-password")
def forgot_password(request: ForgotPasswordRequest):
    # В реальном проекте: генерация токена сброса и отправка на email/phone.
    # Здесь просто заглушка.
    return {"message": "If account exists, a reset link has been sent."}

@router.post("/reset-password")
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    # В реальности нужно проверить reset-токен (хранимый в БД),
    # найти пользователя и обновить пароль.
    # Здесь упрощённо: токен должен быть валидным JWT (заглушка).
    try:
        payload = jwt.decode(request.token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")

    user = user_methods.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    hashed = pwd_context.hash(request.new_password)
    user_methods.update_user_password(db, user_id, hashed)
    return {"message": "Password reset successfully"}

@router.get("/me", response_model=UserProfileResponse)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user