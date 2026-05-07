from sqlalchemy.orm import Session
from typing import List

from .. import models

from .base import safe_commit

def create_doctor(db: Session, payload: dict):
    doctor = models.Doctor(**payload)
    db.add(doctor)
    safe_commit(db)
    db.refresh(doctor)
    return doctor

def update_doctor(db: Session, doctor_id: int, payload: dict):
    doctor = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    if not doctor:
        return None
    for key, value in payload.items():
        if hasattr(doctor, key):
            setattr(doctor, key, value)
    safe_commit(db)
    db.refresh(doctor)
    return doctor

def archive_doctor(db: Session, doctor_id: int):
    doctor = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    if doctor:
        doctor.is_active = False
        safe_commit(db)
        return True
    return False
def list_doctors(db: Session):
    return db.query(models.Doctor).filter(models.Doctor.is_active.is_(True)).all()


def get_doctor_by_id(db: Session, doctor_id: int):
    return db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()


def get_available_slots(db: Session, doctor_id: int, date):
    return db.query(models.DoctorSchedule).filter(
        models.DoctorSchedule.doctor_id == doctor_id,
        models.DoctorSchedule.work_date == date,
        models.DoctorSchedule.is_available.is_(True)
    ).all()