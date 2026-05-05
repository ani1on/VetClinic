from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import datamodels as schemas
from ..dependencies import get_db, get_current_user, get_current_admin
from ...database.crud.order import (
    create_order_from_cart,
    list_user_orders,
    get_order_by_id,
    update_order_status
)

router = APIRouter(prefix="/api/orders", tags=["orders"])

@router.post("/", response_model=schemas.order.OrderResponse, status_code=status.HTTP_201_CREATED)
def create(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        order = create_order_from_cart(db, current_user.id)
        if not order:
            raise HTTPException(status_code=400, detail="Корзина пуста или недостаточно товаров")
        return order
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[schemas.order.OrderResponse])
def list_orders(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    return list_user_orders(db, current_user.id)

@router.get("/{order_id}", response_model=schemas.order.OrderResponse)
def get_order(order_id: int, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    order = get_order_by_id(db, order_id)
    if not order or order.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    return order

@router.patch("/{order_id}/status", response_model=schemas.order.OrderResponse)
def change_status(order_id: int, status_update: schemas.order.OrderStatusUpdate, admin = Depends(get_current_admin), db: Session = Depends(get_db)):
    order = update_order_status(db, order_id, status_update.status)
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    return order