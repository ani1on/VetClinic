from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import datamodels as schemas
from ..dependencies import get_db, get_current_admin
from ...database.crud.news import (
    list_news,
    get_news_by_id,
    create_news,
    update_news,
    delete_news
)

router = APIRouter(prefix="/api/news", tags=["news"])

@router.get("/", response_model=schemas.news.NewsListResponse)
def get_news(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    news = list_news(db)
    total = len(news)
    return {"total": total, "news": news[skip:skip+limit]}

@router.post("/", response_model=schemas.news.NewsResponse, status_code=status.HTTP_201_CREATED)
def create(payload: schemas.news.NewsCreateRequest, admin = Depends(get_current_admin), db: Session = Depends(get_db)):
    return create_news(db, payload.dict())

@router.put("/{news_id}", response_model=schemas.news.NewsResponse)
def update(news_id: int, payload: schemas.news.NewsUpdateRequest, admin = Depends(get_current_admin), db: Session = Depends(get_db)):
    news = update_news(db, news_id, payload.dict(exclude_unset=True))
    if not news:
        raise HTTPException(status_code=404, detail="Новость не найдена")
    return news

@router.delete("/{news_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(news_id: int, admin = Depends(get_current_admin), db: Session = Depends(get_db)):
    if not delete_news(db, news_id):
        raise HTTPException(status_code=404, detail="Новость не найдена")
    return