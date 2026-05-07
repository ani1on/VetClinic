from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import datamodels as schemas
from ..dependencies import get_db, get_current_admin
from ...database.crud.services import (
    list_services,
    get_service_by_id,
    create_service,
    update_service,
    delete_service
)

router = APIRouter(prefix="/api/services", tags=["services"])

@router.get("/", response_model=List[schemas.service.ServiceResponse])
def get_services(db: Session = Depends(get_db)):
    return list_services(db)

@router.get("/{service_id}", response_model=schemas.service.ServiceResponse)
def get_service(service_id: int, db: Session = Depends(get_db)):
    service = get_service_by_id(db, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Услуга не найдена")
    return service

@router.post("/", response_model=schemas.service.ServiceResponse, status_code=status.HTTP_201_CREATED)
def create(payload: schemas.service.ServiceCreateRequest, admin = Depends(get_current_admin), db: Session = Depends(get_db)):
    return create_service(db, payload.dict())

@router.put("/{service_id}", response_model=schemas.service.ServiceResponse)
def update(service_id: int, payload: schemas.service.ServiceUpdateRequest, admin = Depends(get_current_admin), db: Session = Depends(get_db)):
    service = update_service(db, service_id, payload.dict(exclude_unset=True))
    if not service:
        raise HTTPException(status_code=404, detail="Услуга не найдена")
    return service

@router.delete("/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(service_id: int, admin = Depends(get_current_admin), db: Session = Depends(get_db)):
    if not delete_service(db, service_id):
        raise HTTPException(status_code=404, detail="Услуга не найдена")
    return