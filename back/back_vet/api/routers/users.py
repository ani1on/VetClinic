from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from .. import datamodels as schemas
from ..dependencies import get_db, get_current_user, get_current_admin
from ...database.crud.user import get_user_by_id, update_user_profile, list_users
from ...database.crud.pet import get_user_pets

router = APIRouter(prefix="/api/users", tags=["users"])

@router.get("/profile", response_model=schemas.user.UserProfileResponse)
def get_profile(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    pets = get_user_pets(db, current_user.id)
    return {
        "id": current_user.id,
        "name": current_user.name,
        "phone": current_user.phone,
        "email": current_user.email,
        "pets": pets
    }

@router.put("/profile", response_model=schemas.user.UserDetailResponse)
def update_profile(
    payload: schemas.user.UserUpdateRequest,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = update_user_profile(db, current_user.id, payload.dict(exclude_unset=True))
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user

@router.get("/{user_id}", response_model=schemas.user.UserDetailResponse)
def get_user(user_id: int, admin = Depends(get_current_admin), db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user

@router.get("/", response_model=schemas.user.UserListResponse)
def list_users_view(
    name: Optional[str] = None,
    role: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    filters = {}
    if name:
        filters["name"] = name
    if role:
        filters["role"] = role
    users = list_users(db, filters)
    total = len(users)
    return {"total": total, "users": users[skip:skip+limit]}