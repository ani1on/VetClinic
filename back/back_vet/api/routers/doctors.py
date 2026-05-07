from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import date
from typing import List

from .. import datamodels as schemas
from ..dependencies import get_db, get_current_admin
from ...database.crud.doctor import (
    list_doctors,
    get_doctor_by_id,
    get_available_slots,
    create_doctor,
    update_doctor,
    archive_doctor
)
from ...database import models              # импорт всех моделей
from ...database.models.user import User    # конкретно User для проверки

router = APIRouter(prefix="/api/doctors", tags=["doctors"])

# ---------- Публичные эндпоинты ----------
@router.get("/", response_model=List[schemas.doctor.DoctorResponse])
def get_doctors(db: Session = Depends(get_db)):
    return list_doctors(db)

@router.get("/{doctor_id}", response_model=schemas.doctor.DoctorDetailResponse)
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = get_doctor_by_id(db, doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Врач не найден")
    return doctor

@router.get("/{doctor_id}/slots", response_model=List[schemas.doctor.SlotResponse])
def doctor_slots(
    doctor_id: int,
    date: date = Query(..., description="Дата YYYY-MM-DD"),
    db: Session = Depends(get_db)
):
    schedules = get_available_slots(db, doctor_id, date)
    slots = []
    for s in schedules:
        import datetime
        cur = s.start_time
        while cur < s.end_time:
            slots.append({"time": cur, "available": True})
            cur = (datetime.datetime.combine(date, cur) + datetime.timedelta(minutes=s.slot_duration)).time()
    return slots

# ---------- Административные эндпоинты ----------
@router.post("/", response_model=schemas.doctor.DoctorResponse, status_code=status.HTTP_201_CREATED)
def create(payload: schemas.doctor.DoctorCreateRequest, admin = Depends(get_current_admin), db: Session = Depends(get_db)):
    # Проверка существования пользователя
    user = db.query(User).get(payload.user_id)
    if not user:
        raise HTTPException(status_code=400, detail="Пользователь не найден")
    # Проверка, что такой врач ещё не привязан к этому пользователю
    existing = db.query(models.Doctor).filter(models.Doctor.user_id == payload.user_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Врач для этого пользователя уже существует")
    return create_doctor(db, payload.dict())

@router.put("/{doctor_id}", response_model=schemas.doctor.DoctorResponse)
def update(doctor_id: int, payload: schemas.doctor.DoctorUpdateRequest, admin = Depends(get_current_admin), db: Session = Depends(get_db)):
    doctor = update_doctor(db, doctor_id, payload.dict(exclude_unset=True))
    if not doctor:
        raise HTTPException(status_code=404, detail="Врач не найден")
    return doctor

@router.delete("/{doctor_id}", status_code=status.HTTP_204_NO_CONTENT)
def archive(doctor_id: int, admin = Depends(get_current_admin), db: Session = Depends(get_db)):
    if not archive_doctor(db, doctor_id):
        raise HTTPException(status_code=404, detail="Врач не найден")
    return