from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import datamodels as schemas
from ..dependencies import get_db, get_current_user
from ...database.crud.pet import (
    create_pet,
    get_user_pets,
    get_pet_by_id,
    update_pet,
    delete_pet,
    get_pet_medical_history
)

router = APIRouter(prefix="/api/pets", tags=["pets"])

@router.post("/", response_model=schemas.pet.PetResponse, status_code=status.HTTP_201_CREATED)
def create(payload: schemas.pet.PetCreateRequest, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    return create_pet(db, current_user.id, payload.dict())

@router.get("/", response_model=List[schemas.pet.PetResponse])
def list_pets(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_user_pets(db, current_user.id)

@router.get("/{pet_id}", response_model=schemas.pet.PetResponse)
def get_pet(pet_id: int, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    pet = get_pet_by_id(db, pet_id)
    if not pet or pet.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Питомец не найден")
    return pet

@router.put("/{pet_id}", response_model=schemas.pet.PetResponse)
def update(pet_id: int, payload: schemas.pet.PetUpdateRequest, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    pet = get_pet_by_id(db, pet_id)
    if not pet or pet.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Питомец не найден")
    return update_pet(db, pet_id, payload.dict(exclude_unset=True))

@router.delete("/{pet_id}", status_code=status.HTTP_204_NO_CONTENT)
def archive(pet_id: int, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    pet = get_pet_by_id(db, pet_id)
    if not pet or pet.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Питомец не найден")
    delete_pet(db, pet_id)
    return

@router.get("/{pet_id}/history", response_model=List[schemas.pet.MedicalRecordResponse])
def history(pet_id: int, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    pet = get_pet_by_id(db, pet_id)
    if not pet or pet.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Питомец не найден")
    return get_pet_medical_history(db, pet_id)