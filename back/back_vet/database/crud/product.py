from sqlalchemy.orm import Session
from .. import models
from .base import safe_commit


def list_products(db: Session):
    return db.query(models.Product).filter(models.Product.is_available.is_(True)).all()


def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def get_product_by_id(db: Session, product_id: int):
    """Возвращает товар по ID (аналог get_product)."""
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def create_product(db: Session, payload: dict):
    product = models.Product(**payload)
    db.add(product)
    safe_commit(db)
    db.refresh(product)
    return product


def update_product(db: Session, product_id: int, payload: dict):
    """
    Частичное обновление товара.
    payload – словарь с изменяемыми полями (например, {"name": "...", "price": ...}).
    Возвращает обновлённый объект или None.
    """
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        return None

    for key, value in payload.items():
        if hasattr(product, key):
            setattr(product, key, value)

    safe_commit(db)
    db.refresh(product)
    return product


def update_product_stock(db: Session, product_id: int, quantity: int):
    """
    Устанавливает новое количество товара на складе.
    Возвращает обновлённый объект или None.
    """
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        return None

    product.stock_quantity = quantity
    safe_commit(db)
    db.refresh(product)
    return product


def delete_product(db: Session, product_id: int):
    """
    Мягкое удаление: делает товар недоступным (is_available = False).
    Возвращает обновлённый объект или None.
    """
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        return None

    product.is_available = False
    safe_commit(db)
    db.refresh(product)
    return product