from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy.orm import Session

from .. import models
from .base import safe_commit


def create_user(db: Session, name: str, phone: str, email: str, password_hash: str, role: str = "client",
                utm_source: str = None, utm_medium: str = None, utm_campaign: str = None,
                utm_term: str = None, utm_content: str = None):
    user = models.User(
        name=name,
        phone=phone,
        email=email,
        password_hash=password_hash,
        role=role,
        utm_source=utm_source,
        utm_medium=utm_medium,
        utm_campaign=utm_campaign,
        utm_term=utm_term,
        utm_content=utm_content,
    )
    db.add(user)
    safe_commit(db)
    db.refresh(user)
    return user

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def find_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def find_user_by_phone(db: Session, phone: str):
    return db.query(models.User).filter(models.User.phone == phone).first()


def update_user_profile(db: Session, user_id: int, payload: dict):
    user = get_user_by_id(db, user_id)
    if not user:
        return None

    for key, value in payload.items():
        if hasattr(user, key):
            setattr(user, key, value)

    safe_commit(db)
    db.refresh(user)
    return user


def list_users(db: Session, filters: dict = None):
    q = db.query(models.User)

    if filters:
        if "name" in filters:
            q = q.filter(models.User.name.ilike(f"%{filters['name']}%"))
        if "role" in filters:
            q = q.filter(models.User.role == filters["role"])

    return q.all()


def save_refresh_token(db: Session, user_id: int, token: str, expires_at: datetime):
    rt = models.RefreshToken(user_id=user_id, token=token, expires_at=expires_at)
    db.add(rt)
    safe_commit(db)
    return rt


def validate_refresh_token(db: Session, token: str):
    return db.query(models.RefreshToken).filter(
        models.RefreshToken.token == token,
        models.RefreshToken.revoked.is_(False),
        models.RefreshToken.expires_at > datetime.now(timezone.utc)
    ).first()


def update_user_role(db: Session, user_id: int, new_role: str) -> models.User | None:

    allowed_roles = {'client', 'admin'}
    if new_role not in allowed_roles:
        raise ValueError(f"Недопустимая роль. Разрешены: {', '.join(allowed_roles)}")

    user = get_user_by_id(db, user_id)
    if not user:
        return None

    user.role = new_role
    safe_commit(db)
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int) -> bool:

    user = get_user_by_id(db, user_id)
    if not user:
        return False


    db.query(models.RefreshToken).filter(models.RefreshToken.user_id == user_id).delete()

    db.delete(user)
    safe_commit(db)
    return True