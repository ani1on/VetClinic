from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session

from .. import datamodels as schemas
from ..dependencies import get_db, get_current_user
from ..utils.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token
)
from ...database.crud.user import (
    create_user,
    find_user_by_email,
    find_user_by_phone,
    get_user_by_id,
    save_refresh_token,
    validate_refresh_token
)
from ...database.models.user import RefreshToken

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register", response_model=schemas.auth.AuthResponse)
def register(request: schemas.auth.RegisterRequest, db: Session = Depends(get_db)):
    if request.email and find_user_by_email(db, request.email):
        raise HTTPException(status_code=400, detail="Email уже используется")
    if find_user_by_phone(db, request.phone):
        raise HTTPException(status_code=400, detail="Телефон уже используется")

    hashed = get_password_hash(request.password)
    user = create_user(
        db, name=request.name, phone=request.phone,
        email=request.email, password_hash=hashed,
        role=request.role or "client",
        utm_source=request.utm_source,
        utm_medium=request.utm_medium,
        utm_campaign=request.utm_campaign,
        utm_term=request.utm_term,
        utm_content=request.utm_content,
    )

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)
    expires_at = datetime.now(timezone.utc) + timedelta(days=30)
    save_refresh_token(db, user.id, refresh_token, expires_at)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": user
    }

@router.post("/login", response_model=schemas.auth.AuthResponse)
def login(request: schemas.auth.LoginRequest, db: Session = Depends(get_db)):
    user = find_user_by_email(db, request.login) if "@" in request.login else find_user_by_phone(db, request.login)
    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Неверные учётные данные")

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)
    expires_at = datetime.now(timezone.utc) + timedelta(days=30)
    save_refresh_token(db, user.id, refresh_token, expires_at)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": user
    }

@router.post("/refresh", response_model=schemas.auth.TokenResponse)
def refresh_token(request: schemas.auth.RefreshRequest, db: Session = Depends(get_db)):
    token_record = validate_refresh_token(db, request.refresh_token)
    if not token_record:
        raise HTTPException(status_code=401, detail="Недействительный refresh токен")

    token_record.revoked = True
    db.commit()

    user_id = token_record.user_id
    new_access = create_access_token(user_id)
    new_refresh = create_refresh_token(user_id)
    expires_at = datetime.now(timezone.utc) + timedelta(days=30)
    save_refresh_token(db, user_id, new_refresh, expires_at)

    return {
        "access_token": new_access,
        "refresh_token": new_refresh,
        "token_type": "bearer"
    }

@router.post("/logout")
def logout(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    db.query(RefreshToken).filter(
        RefreshToken.user_id == current_user.id,
        RefreshToken.revoked == False
    ).update({"revoked": True})
    db.commit()
    return {"detail": "Вы вышли из системы"}

@router.post("/forgot-password")
def forgot_password(request: schemas.auth.ForgotPasswordRequest):
    return {"detail": "Инструкции отправлены (заглушка)"}

@router.post("/reset-password")
def reset_password(request: schemas.auth.ResetPasswordRequest):
    return {"detail": "Пароль изменён (заглушка)"}

@router.get("/me", response_model=schemas.auth.UserProfileResponse)
def read_current_user(current_user = Depends(get_current_user)):
    return current_user