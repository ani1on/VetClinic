# back_vet/api/routers/token.py
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone

from ..dependencies import get_db
from ..utils.security import verify_password, create_access_token, create_refresh_token
from ...database.crud.user import find_user_by_email, find_user_by_phone, save_refresh_token

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/token")
async def login_for_access_token(request: Request, db: Session = Depends(get_db)):
    # Получаем данные из формы (x-www-form-urlencoded)
    form = await request.form()
    username = form.get("username")   # email или телефон
    password = form.get("password")

    if not username or not password:
        raise HTTPException(status_code=400, detail="Необходимы username и password")

    user = find_user_by_email(db, username) if "@" in username else find_user_by_phone(db, username)
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Неверные учётные данные")

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)
    expires_at = datetime.now(timezone.utc) + timedelta(days=30)
    save_refresh_token(db, user.id, refresh_token, expires_at)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }