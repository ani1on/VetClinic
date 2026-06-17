from sqlalchemy.orm import Session
from .. import models
from .base import safe_commit


def get_cart(db: Session, user_id: int):
    return db.query(models.CartItem).filter(models.CartItem.user_id == user_id).all()


def add_cart_item(db: Session, user_id: int, product_id: int, quantity: int):
    existing = db.query(models.CartItem).filter(
        models.CartItem.user_id == user_id,
        models.CartItem.product_id == product_id
    ).first()
    if existing:
        existing.quantity += quantity
        safe_commit(db)
        db.refresh(existing)
        return existing
    item = models.CartItem(user_id=user_id, product_id=product_id, quantity=quantity)
    db.add(item)
    safe_commit(db)
    db.refresh(item)
    return item


def update_cart_item(db: Session, item_id: int, quantity: int, user_id: int):
    item = db.query(models.CartItem).filter(
        models.CartItem.id == item_id,
        models.CartItem.user_id == user_id
    ).first()
    if item:
        item.quantity = quantity
        safe_commit(db)
        db.refresh(item)
    return item


def remove_cart_item(db: Session, item_id: int, user_id: int):
    item = db.query(models.CartItem).filter(
        models.CartItem.id == item_id,
        models.CartItem.user_id == user_id
    ).first()
    if item:
        db.delete(item)
        safe_commit(db)
        return True
    return False


def create_order(db: Session, user_id: int):

    cart = get_cart(db, user_id)

    if not cart:
        return None

    total = 0
    items = []

    for c in cart:
        product = db.get(models.Product, c.product_id)

        if not product or product.stock_quantity < c.quantity:
            raise ValueError("Stock error")

        total += product.price * c.quantity

        items.append(models.OrderItem(
            product_id=product.id,
            quantity=c.quantity,
            price_per_unit=product.price
        ))

        product.stock_quantity -= c.quantity
        db.delete(c)

    order = models.Order(user_id=user_id, total_amount=total)
    order.items = items

    db.add(order)
    safe_commit(db)
    db.refresh(order)

    return order


def create_order_from_cart(db: Session, user_id: int):

    return create_order(db, user_id)


def list_user_orders(db: Session, user_id: int):

    return db.query(models.Order).filter(models.Order.user_id == user_id).all()


def get_order_by_id(db: Session, order_id: int):

    return db.query(models.Order).filter(models.Order.id == order_id).first()


def update_order_status(db: Session, order_id: int, status: str):

    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        return None
    order.status = status
    safe_commit(db)
    db.refresh(order)
    return order