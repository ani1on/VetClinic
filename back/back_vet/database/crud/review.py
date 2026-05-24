from sqlalchemy.orm import Session
from .. import models
from .base import safe_commit
from sqlalchemy.orm import joinedload

def create_review(db: Session, user_id: int, payload: dict):
    review = models.Review(user_id=user_id, **payload)
    db.add(review)
    safe_commit(db)
    db.refresh(review)
    return review


def list_reviews(db: Session, status: str = None):
    q = db.query(models.Review).options(joinedload(models.Review.user))
    if status:
        q = q.filter(models.Review.status == status)
    return q.all()

def moderate_review(db: Session, review_id: int, status: str):

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

def delete_review(db: Session, review_id: int, user_id: int, is_admin: bool = False) -> bool:
    review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if not review:
        return False
    db.delete(review)
    safe_commit(db)
    return True