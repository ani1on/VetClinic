from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date
from typing import List

from .. import datamodels as schemas
from ..dependencies import get_db
from ...database.crud.doctor import list_doctors, get_doctor_by_id, get_available_slots

router = APIRouter(prefix="/api/doctors", tags=["doctors"])

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
    date: date = Query(..., description="Дата в формате YYYY-MM-DD"),
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