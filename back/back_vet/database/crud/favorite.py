from sqlalchemy.orm import Session
from .. import models
from .base import safe_commit


def list_user_favorites(db: Session, user_id: int):
    """
    Возвращает список избранных товаров пользователя.
    Возвращается список объектов Favorite (с подгруженным продуктом).
    """
    return (
        db.query(models.Favorite)
        .filter(models.Favorite.user_id == user_id)
        .all()
    )


def add_favorite(db: Session, user_id: int, product_id: int):
    """
    Добавляет товар в избранное пользователя.
    Если запись уже существует – возвращает её без повторного создания.
    Возвращает объект Favorite.
    """
    # Проверяем, не добавлен ли уже этот товар в избранное
    existing = (
        db.query(models.Favorite)
        .filter(
            models.Favorite.user_id == user_id,
            models.Favorite.product_id == product_id,
        )
        .first()
    )
    if existing:
        return existing

    favorite = models.Favorite(user_id=user_id, product_id=product_id)
    db.add(favorite)
    safe_commit(db)
    db.refresh(favorite)
    return favorite


def remove_favorite(db: Session, user_id: int, product_id: int):
    """
    Удаляет товар из избранного пользователя.
    Возвращает True, если удаление выполнено, иначе False.
    """
    favorite = (
        db.query(models.Favorite)
        .filter(
            models.Favorite.user_id == user_id,
            models.Favorite.product_id == product_id,
        )
        .first()
    )
    if not favorite:
        return False

    db.delete(favorite)
    safe_commit(db)
    return True


def exists_favorite(db: Session, user_id: int, product_id: int) -> bool:
    """
    Проверяет, находится ли товар в избранном у пользователя.
    Возвращает True/False.
    """
    return (
        db.query(models.Favorite)
        .filter(
            models.Favorite.user_id == user_id,
            models.Favorite.product_id == product_id,
        )
        .first()
        is not None
    )