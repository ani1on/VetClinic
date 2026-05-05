from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import datamodels as schemas
from ..dependencies import get_db, get_current_user, get_current_admin
from ...database.crud.appointment import (
    create_appointment,
    list_user_appointments,
    get_appointment_by_id,
    update_appointment,
    update_appointment_status,
    cancel_appointment,
    list_all_appointments
)

router = APIRouter(prefix="/api/appointments", tags=["appointments"])

@router.post("/", response_model=schemas.appointment.AppointmentResponse, status_code=status.HTTP_201_CREATED)
def create(payload: schemas.appointment.AppointmentCreateRequest, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    return create_appointment(db, current_user.id, payload.dict())

@router.get("/", response_model=List[schemas.appointment.AppointmentResponse])
def list_my(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    return list_user_appointments(db, current_user.id)

@router.get("/{appointment_id}", response_model=schemas.appointment.AppointmentResponse)
def get_one(appointment_id: int, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    appt = get_appointment_by_id(db, appointment_id)
    if not appt or appt.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Запись не найдена")
    return appt

@router.put("/{appointment_id}", response_model=schemas.appointment.AppointmentResponse)
def update(appointment_id: int, payload: schemas.appointment.AppointmentUpdateRequest, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    appt = get_appointment_by_id(db, appointment_id)
    if not appt or appt.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Запись не найдена")
    return update_appointment(db, appointment_id, payload.dict(exclude_unset=True))

@router.patch("/{appointment_id}/status", response_model=schemas.appointment.AppointmentResponse)
def change_status(appointment_id: int, status_update: schemas.appointment.AppointmentStatusUpdate, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    appt = get_appointment_by_id(db, appointment_id)
    if not appt or appt.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Запись не найдена")
    return update_appointment_status(db, appointment_id, status_update.status)

@router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel(appointment_id: int, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    appt = get_appointment_by_id(db, appointment_id)
    if not appt or appt.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Запись не найдена")
    cancel_appointment(db, appointment_id)
    return

@router.get("/admin/all", response_model=List[schemas.appointment.AppointmentResponse])
def admin_list(admin = Depends(get_current_admin), db: Session = Depends(get_db)):
    return list_all_appointments(db)