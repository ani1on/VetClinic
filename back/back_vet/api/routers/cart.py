from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import datamodels as schemas
from ..dependencies import get_db, get_current_user
from ...database.crud.order import (
    get_cart,
    add_cart_item,
    update_cart_item,
    remove_cart_item
)

router = APIRouter(prefix="/api/cart", tags=["cart"])

@router.get("/", response_model=schemas.cart.CartResponse)
def view_cart(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    items = get_cart(db, current_user.id)
    total = sum(item.product.price * item.quantity for item in items if item.product)
    return {"items": items, "total_price": total}

@router.post("/items", response_model=schemas.cart.CartItemResponse, status_code=status.HTTP_201_CREATED)
def add_item(payload: schemas.cart.CartItemCreateRequest, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    return add_cart_item(db, current_user.id, payload.product_id, payload.quantity)

@router.put("/items/{item_id}", response_model=schemas.cart.CartItemResponse)
def update_item(item_id: int, payload: schemas.cart.CartItemUpdateRequest, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    item = update_cart_item(db, item_id, payload.quantity, user_id=current_user.id)
    if not item:
        raise HTTPException(status_code=404, detail="Элемент корзины не найден")
    return item

@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    if not remove_cart_item(db, item_id, current_user.id):
        raise HTTPException(status_code=404, detail="Элемент корзины не найден")
    return