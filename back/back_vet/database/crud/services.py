from sqlalchemy.orm import Session
from .base import safe_commit
from .. import models


def list_services(db: Session):
    return db.query(models.Service).filter(models.Service.is_active.is_(True)).all()


def create_service(db: Session, payload: dict):
    service = models.Service(**payload)
    db.add(service)
    safe_commit(db)
    db.refresh(service)
    return service


def get_service_by_id(db: Session, service_id: int):
    """Возвращает услугу по ID независимо от статуса is_active."""
    return db.query(models.Service).filter(models.Service.id == service_id).first()


def update_service(db: Session, service_id: int, payload: dict):
    """
    Частичное обновление услуги.
    payload – словарь с полями для обновления (например, {"name": "...", "price": ...}).
    Возвращает обновлённый объект или None, если услуга не найдена.
    """
    service = db.query(models.Service).filter(models.Service.id == service_id).first()
    if not service:
        return None

    for key, value in payload.items():
        if hasattr(service, key):
            setattr(service, key, value)

    safe_commit(db)
    db.refresh(service)
    return service


def delete_service(db: Session, service_id: int):
    """
    Мягкое удаление: устанавливает is_active в False.
    Возвращает объект услуги после изменения или None, если услуга не найдена.
    """
    service = db.query(models.Service).filter(models.Service.id == service_id).first()
    if not service:
        return None

    service.is_active = False
    safe_commit(db)
    db.refresh(service)
    return service