from sqlalchemy.orm import Session
from datetime import datetime
from .. import models
from .base import safe_commit


def list_news(db: Session):
    return db.query(models.News).filter(models.News.is_published.is_(True)).all()


def create_news(db: Session, payload: dict):
    news = models.News(**payload)
    db.add(news)
    safe_commit(db)
    db.refresh(news)
    return news


def get_news_by_id(db: Session, news_id: int):
    """Возвращает новость по ID, независимо от статуса публикации."""
    return db.query(models.News).filter(models.News.id == news_id).first()


def update_news(db: Session, news_id: int, payload: dict):
    """
    Частичное обновление новости.
    Автоматически устанавливает updated_at = datetime.utcnow().
    Возвращает обновлённый объект или None.
    """
    news = db.query(models.News).filter(models.News.id == news_id).first()
    if not news:
        return None

    for key, value in payload.items():
        if hasattr(news, key):
            setattr(news, key, value)

    news.updated_at = datetime.utcnow()
    safe_commit(db)
    db.refresh(news)
    return news


def delete_news(db: Session, news_id: int):
    """
    Мягкое удаление: снимает с публикации (is_published = False).
    Возвращает обновлённый объект или None.
    """
    news = db.query(models.News).filter(models.News.id == news_id).first()
    if not news:
        return None

    news.is_published = False
    safe_commit(db)
    db.refresh(news)
    return news