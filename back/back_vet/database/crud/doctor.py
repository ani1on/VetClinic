from sqlalchemy.orm import Session
from typing import List

from .. import models


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