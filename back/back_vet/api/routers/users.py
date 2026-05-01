from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from back.back_vet.database.core import get_db
from back.back_vet.database.methods import user_methods
from ..datamodels.user import (
    UserProfileResponse,
    UserUpdateRequest,
    UserDetailResponse,
    UserListResponse,
)
from ..dependencies import get_current_user, get_current_admin_user
from ...database.models import User

router = APIRouter(prefix="/api", tags=["users"])

@router.get("/users/profile", response_model=UserProfileResponse)
def get_my_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Возвращает профиль текущего пользователя вместе с его питомцами.
    """
    # Загружаем профиль с питомцами через специальный метод
    user = user_methods.get_profile_with_pets(db, current_user.id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/users/profile", response_model=UserProfileResponse)
def update_my_profile(
    updates: UserUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Обновляет данные текущего пользователя (name, phone, email).
    """
    # Убираем поля, которые не были переданы
    update_data = updates.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No data to update")

    # Проверяем уникальность телефона/email при изменении
    if "phone" in update_data and update_data["phone"] != current_user.phone:
        existing = user_methods.find_user_by_phone(db, update_data["phone"])
        if existing:
            raise HTTPException(status_code=400, detail="Phone already used")
    if "email" in update_data and update_data["email"] != current_user.email:
        existing = user_methods.find_user_by_email(db, update_data["email"])
        if existing:
            raise HTTPException(status_code=400, detail="Email already used")

    updated_user = user_methods.update_user_profile(db, current_user.id, update_data)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.get("/users", response_model=UserListResponse)
def list_all_users(
    name: Optional[str] = Query(None),
    phone: Optional[str] = Query(None),
    role: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin_user)   # только для админов
):
    """
    Администратор получает список пользователей с фильтрацией и пагинацией.
    """
    filters = {}
    if name:
        filters["name"] = name
    if phone:
        filters["phone"] = phone
    if role:
        filters["role"] = role

    users = user_methods.list_users(db, filters=filters, skip=skip, limit=limit)
    # В реальном проекте нужно ещё общее количество для пагинации,
    # здесь упрощённо: вернём только список
    return UserListResponse(users=users, total=len(users))

@router.get("/users/{user_id}", response_model=UserDetailResponse)
def get_user_details(
    user_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin_user)
):
    """
    Администратор получает детальную информацию о любом пользователе.
    """
    user = user_methods.get_user_details(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user