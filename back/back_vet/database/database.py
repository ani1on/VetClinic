from datetime import date, datetime, timedelta
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_, or_
from ..database import models

# =========================== AUTH ===========================
def create_user(db: Session, name: str, phone: str, email: str, password_hash: str, role: str = "client") -> models.User:
    db_user = models.User(name=name, phone=phone, email=email, password_hash=password_hash, role=role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def find_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()

def find_user_by_phone(db: Session, phone: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.phone == phone).first()

def get_user_by_id(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()

def save_refresh_token(db: Session, user_id: int, token: str, expires_at: datetime):
    rt = models.RefreshToken(user_id=user_id, token=token, expires_at=expires_at)
    db.add(rt)
    db.commit()
    return rt

def validate_refresh_token(db: Session, token: str) -> Optional[models.RefreshToken]:
    return db.query(models.RefreshToken).filter(
        models.RefreshToken.token == token,
        models.RefreshToken.revoked == False,
        models.RefreshToken.expires_at > datetime.utcnow()
    ).first()

def revoke_refresh_token(db: Session, token: str):
    rt = db.query(models.RefreshToken).filter(models.RefreshToken.token == token).first()
    if rt:
        rt.revoked = True
        db.commit()

def update_user_password(db: Session, user_id: int, new_password_hash: str):
    user = get_user_by_id(db, user_id)
    if user:
        user.password_hash = new_password_hash
        db.commit()

# ========================= USERS / PROFILE =========================
def get_profile_with_pets(db: Session, user_id: int) -> Optional[models.User]:
    """Возвращает пользователя с его питомцами (жадная загрузка)."""
    return db.query(models.User).filter(models.User.id == user_id).first()
    # relationship pets уже загружается лениво; для явной подгрузки можно использовать
    # .options(joinedload(models.User.pets))

def update_user_profile(db: Session, user_id: int, payload: dict):
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    for key, value in payload.items():
        if hasattr(user, key):
            setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

def list_users(db: Session, filters: dict = None, skip: int = 0, limit: int = 100) -> List[models.User]:
    q = db.query(models.User)
    if filters:
        if 'name' in filters:
            q = q.filter(models.User.name.ilike(f"%{filters['name']}%"))
        if 'phone' in filters:
            q = q.filter(models.User.phone == filters['phone'])
        if 'role' in filters:
            q = q.filter(models.User.role == filters['role'])
    return q.offset(skip).limit(limit).all()

def get_user_details(db: Session, user_id: int) -> Optional[models.User]:
    return get_user_by_id(db, user_id)