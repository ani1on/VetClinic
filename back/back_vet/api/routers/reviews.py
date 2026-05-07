from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import datamodels as schemas
from ..dependencies import get_db, get_current_user, get_current_admin
from ...database.crud.review import create_review, list_reviews, moderate_review

router = APIRouter(prefix="/api/reviews", tags=["reviews"])

@router.get("/", response_model=schemas.review.ReviewListResponse)
def get_reviews(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    reviews = list_reviews(db)
    return {"total": len(reviews), "reviews": reviews[skip:skip+limit]}

@router.post("/", response_model=schemas.review.ReviewResponse)
def create(payload: schemas.review.ReviewCreateRequest, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    return create_review(db, current_user.id, payload.dict())

@router.patch("/{review_id}/moderate", response_model=schemas.review.ReviewResponse)
def moderate(review_id: int, mod: schemas.review.ReviewModerateRequest, admin = Depends(get_current_admin), db: Session = Depends(get_db)):
    review = moderate_review(db, review_id, mod.status)
    if not review:
        raise HTTPException(status_code=404, detail="Отзыв не найден")
    return review