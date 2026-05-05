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
    return db.query(models.Appointment).filter(
        models.Appointment.user_id == user_id
    ).all()


def update_status(db: Session, appointment_id: int, status: str):
    appt = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if appt:
        appt.status = status
        safe_commit(db)


def get_appointment_by_id(db: Session, appointment_id: int):
    """Возвращает запись о приёме по ID или None."""
    return db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()


def update_appointment(db: Session, appointment_id: int, payload: dict):
    """
    Частичное обновление полей записи о приёме.
    payload может содержать любые изменяемые поля, кроме id.
    Возвращает обновлённый объект или None, если запись не найдена.
    """
    appt = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not appt:
        return None

    for key, value in payload.items():
        if hasattr(appt, key):
            setattr(appt, key, value)

    safe_commit(db)
    db.refresh(appt)
    return appt


def update_appointment_status(db: Session, appointment_id: int, status: str):
    """
    Обновляет статус записи и возвращает обновлённый объект (или None).
    """
    appt = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not appt:
        return None
    appt.status = status
    safe_commit(db)
    db.refresh(appt)
    return appt


def cancel_appointment(db: Session, appointment_id: int):
    """Отменяет запись (ставит статус 'cancelled') и возвращает обновлённый объект."""
    return update_appointment_status(db, appointment_id, "cancelled")


def list_all_appointments(db: Session):
    """Возвращает все записи о приёмах (для администратора)."""
    return db.query(models.Appointment).all()