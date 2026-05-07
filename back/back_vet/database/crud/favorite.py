from sqlalchemy.orm import Session
from .. import models
from .base import safe_commit


def list_user_favorites(db: Session, user_id: int):
    return db.query(models.Favorite).filter(models.Favorite.user_id == user_id).all()


def add_favorite(db: Session, user_id: int, entity_type: str, entity_id: int):
    fav = models.Favorite(user_id=user_id, entity_type=entity_type, entity_id=entity_id)
    db.add(fav)
    safe_commit(db)
    db.refresh(fav)
    return fav

def remove_favorite(db: Session, favorite_id: int, user_id: int):
    fav = db.query(models.Favorite).filter(
        models.Favorite.id == favorite_id,
        models.Favorite.user_id == user_id
    ).first()
    if fav:
        db.delete(fav)
        safe_commit(db)
        return True
    return False


def exists_favorite(db: Session, user_id: int, entity_type: str, entity_id: int) -> bool:
    return db.query(models.Favorite).filter(
        models.Favorite.user_id == user_id,
        models.Favorite.entity_type == entity_type,
        models.Favorite.entity_id == entity_id
    ).first() is not None