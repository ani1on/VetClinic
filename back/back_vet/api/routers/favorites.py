from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import datamodels as schemas
from ..dependencies import get_db, get_current_user
from ...database.crud.favorite import (
    list_user_favorites,
    add_favorite,
    remove_favorite,
    exists_favorite
)

router = APIRouter(prefix="/api/favorites", tags=["favorites"])

@router.get("/", response_model=List[schemas.favorite.FavoriteResponse])
def get_favorites(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    return list_user_favorites(db, current_user.id)

@router.post("/", response_model=schemas.favorite.FavoriteResponse, status_code=status.HTTP_201_CREATED)
def create_favorite(payload: schemas.favorite.FavoriteCreateRequest, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    if exists_favorite(db, current_user.id, payload.entity_type, payload.entity_id):
        raise HTTPException(status_code=400, detail="Уже в избранном")
    return add_favorite(db, current_user.id, payload.entity_type, payload.entity_id)

@router.delete("/{favorite_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_favorite(favorite_id: int, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    if not remove_favorite(db, favorite_id, current_user.id):
        raise HTTPException(status_code=404, detail="Запись не найдена")
    return