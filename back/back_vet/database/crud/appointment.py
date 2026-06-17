from sqlalchemy.orm import Session
from .. import models
from .base import safe_commit

def create_appointment(db: Session, user_id: int, payload: dict):
    appt = models.Appointment(user_id=user_id, **payload)
    db.add(appt)
    safe_commit(db)
    db.refresh(appt)
    return appt

def list_user_appointments(db: Session, user_id: int):
    appts = db.query(models.Appointment).filter(
        models.Appointment.user_id == user_id
    ).all()
    for a in appts:
        a.pet = db.get(models.Pet, a.pet_id)
        a.service = db.get(models.Service, a.service_id)
        a.doctor = db.get(models.Doctor, a.doctor_id) if a.doctor_id else None
    return appts

def get_appointment_by_id(db: Session, appointment_id: int):
    appt = db.query(models.Appointment).filter(
        models.Appointment.id == appointment_id
    ).first()
    if appt:
        appt.pet = db.get(models.Pet, appt.pet_id)
        appt.service = db.get(models.Service, appt.service_id)
        appt.doctor = db.get(models.Doctor, appt.doctor_id) if appt.doctor_id else None
    return appt

def update_appointment(db: Session, appointment_id: int, payload: dict):
    appt = db.query(models.Appointment).filter(
        models.Appointment.id == appointment_id
    ).first()
    if not appt:
        return None
    for key, value in payload.items():
        if hasattr(appt, key):
            setattr(appt, key, value)
    safe_commit(db)
    db.refresh(appt)
    return appt

def update_appointment_status(db: Session, appointment_id: int, status: str):
    appt = db.query(models.Appointment).filter(
        models.Appointment.id == appointment_id
    ).first()
    if not appt:
        return None
    appt.status = status
    safe_commit(db)
    db.refresh(appt)
    return appt

def cancel_appointment(db: Session, appointment_id: int):
    return update_appointment_status(db, appointment_id, "cancelled")

def list_all_appointments(db: Session):
    appts = db.query(models.Appointment).all()
    for a in appts:
        a.pet = db.get(models.Pet, a.pet_id)
        a.service = db.get(models.Service, a.service_id)
        a.doctor = db.get(models.Doctor, a.doctor_id) if a.doctor_id else None
    return appts