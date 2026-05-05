from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from .. import datamodels as schemas
from ..dependencies import get_db, get_current_admin
from ...database.crud.product import (
    list_products,
    get_product_by_id,
    create_product,
    update_product,
    update_product_stock,
    delete_product
)

router = APIRouter(prefix="/api/products", tags=["products"])

@router.get("/", response_model=schemas.product.ProductListResponse)
def get_products(
    category: Optional[str] = None,
    search: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    in_stock: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    products = list_products(db)
    if category:
        products = [p for p in products if p.category and category.lower() in p.category.lower()]
    if search:
        products = [p for p in products if search.lower() in p.name.lower()]
    if min_price is not None:
        products = [p for p in products if p.price >= min_price]
    if max_price is not None:
        products = [p for p in products if p.price <= max_price]
    if in_stock:
        products = [p for p in products if p.stock_quantity > 0]
    return {"total": len(products), "products": products}

@router.get("/{product_id}", response_model=schemas.product.ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return product

@router.post("/", response_model=schemas.product.ProductResponse, status_code=status.HTTP_201_CREATED)
def create(payload: schemas.product.ProductCreateRequest, admin = Depends(get_current_admin), db: Session = Depends(get_db)):
    return create_product(db, payload.dict())

@router.put("/{product_id}", response_model=schemas.product.ProductResponse)
def update(product_id: int, payload: schemas.product.ProductUpdateRequest, admin = Depends(get_current_admin), db: Session = Depends(get_db)):
    product = update_product(db, product_id, payload.dict(exclude_unset=True))
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return product

@router.patch("/{product_id}/stock", response_model=schemas.product.ProductResponse)
def patch_stock(product_id: int, stock_update: schemas.product.ProductStockUpdate, admin = Depends(get_current_admin), db: Session = Depends(get_db)):
    product = update_product_stock(db, product_id, stock_update.dict(exclude_unset=True))
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(product_id: int, admin = Depends(get_current_admin), db: Session = Depends(get_db)):
    if not delete_product(db, product_id):
        raise HTTPException(status_code=404, detail="Товар не найден")
    return