from sqlalchemy.orm import Session
from typing import List

from .. import models
from .base import safe_commit


def create_pet(db: Session, user_id: int, payload: dict):
    pet = models.Pet(owner_id=user_id, **payload)
    db.add(pet)
    safe_commit(db)
    db.refresh(pet)
    return pet


def get_user_pets(db: Session, user_id: int) -> List[models.Pet]:
    return db.query(models.Pet).filter(
        models.Pet.owner_id == user_id,
        models.Pet.is_archived.is_(False)
    ).all()


def update_pet(db: Session, pet_id: int, payload: dict):
    pet = db.query(models.Pet).filter(models.Pet.id == pet_id).first()
    if not pet:
        return None

    for key, value in payload.items():
        if hasattr(pet, key):
            setattr(pet, key, value)

    safe_commit(db)
    db.refresh(pet)
    return pet


def delete_pet(db: Session, pet_id: int):
    pet = db.query(models.Pet).filter(models.Pet.id == pet_id).first()
    if pet:
        pet.is_archived = True
        safe_commit(db)

def get_pet_by_id(db: Session, pet_id: int):
    return db.query(models.Pet).filter(models.Pet.id == pet_id).first()

def get_pet_medical_history(db: Session, pet_id: int):
    return db.query(models.MedicalRecord).filter(
        models.MedicalRecord.pet_id == pet_id
    ).all()