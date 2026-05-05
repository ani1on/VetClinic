from sqlalchemy.orm import Session
from .. import models
from .base import safe_commit


def get_cart(db: Session, user_id: int):
    return db.query(models.CartItem).filter(models.CartItem.user_id == user_id).all()


def add_cart_item(db: Session, user_id: int, payload: dict):
    """
    Добавляет товар в корзину.
    Если товар уже есть у пользователя – увеличивает количество, иначе создаёт новую запись.
    payload должен содержать product_id (обязательно) и quantity (по умолчанию 1).
    """
    product_id = payload.get("product_id")
    quantity = payload.get("quantity", 1)

    if not product_id:
        raise ValueError("product_id is required")

    existing = (
        db.query(models.CartItem)
        .filter(
            models.CartItem.user_id == user_id,
            models.CartItem.product_id == product_id,
        )
        .first()
    )

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


def update_cart_item(db: Session, cart_item_id: int, payload: dict):
    """
    Обновляет количество товара в корзине по ID записи.
    payload может содержать 'quantity'.
    Возвращает обновлённый объект или None.
    """
    item = db.query(models.CartItem).filter(models.CartItem.id == cart_item_id).first()
    if not item:
        return None

    if "quantity" in payload:
        item.quantity = payload["quantity"]

    safe_commit(db)
    db.refresh(item)
    return item


def remove_cart_item(db: Session, cart_item_id: int):
    """
    Удаляет запись из корзины по ID.
    Возвращает True, если удаление прошло успешно, иначе False.
    """
    item = db.query(models.CartItem).filter(models.CartItem.id == cart_item_id).first()
    if not item:
        return False

    db.delete(item)
    safe_commit(db)
    return True


def create_order(db: Session, user_id: int):
    """Создаёт заказ из текущей корзины пользователя."""
    cart = get_cart(db, user_id)

    if not cart:
        return None

    total = 0
    items = []

    for c in cart:
        product = db.query(models.Product).get(c.product_id)

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
    """Псевдоним для create_order – создаёт заказ из корзины."""
    return create_order(db, user_id)


def list_user_orders(db: Session, user_id: int):
    """Возвращает все заказы пользователя."""
    return db.query(models.Order).filter(models.Order.user_id == user_id).all()


def get_order_by_id(db: Session, order_id: int):
    """Возвращает заказ по ID или None."""
    return db.query(models.Order).filter(models.Order.id == order_id).first()


def update_order_status(db: Session, order_id: int, status: str):
    """
    Обновляет статус заказа.
    Возвращает обновлённый объект или None, если заказ не найден.
    """
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        return None
    order.status = status
    safe_commit(db)
    db.refresh(order)
    return order