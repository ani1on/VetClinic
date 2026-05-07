from sqlalchemy.orm import Session
from .. import models
from .base import safe_commit


def create_review(db: Session, user_id: int, payload: dict):
    review = models.Review(user_id=user_id, **payload)
    db.add(review)
    safe_commit(db)
    db.refresh(review)
    return review


def list_reviews(db: Session):
    return db.query(models.Review).filter(models.Review.status == "approved").all()


def moderate_review(db: Session, review_id: int, status: str):
    """
    Изменяет статус отзыва (модерация).
    Допустимые статусы: 'pending', 'approved', 'rejected'.
    Возвращает обновлённый объект Review или None, если отзыв не найден.
    """
    allowed_statuses = {"pending", "approved", "rejected"}
    if status not in allowed_statuses:
        raise ValueError(f"Invalid status: {status}. Allowed: {', '.join(sorted(allowed_statuses))}")

    review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if not review:
        return None

    review.status = status
    safe_commit(db)
    db.refresh(review)
    return review