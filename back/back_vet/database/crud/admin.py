from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models


def get_dashboard(db: Session):
    week_ago = datetime.utcnow() - timedelta(days=7)

    return {
        "users": db.query(func.count(models.User.id)).scalar(),
        "appointments": db.query(func.count(models.Appointment.id)).scalar(),
        "week_appointments": db.query(func.count(models.Appointment.id)).filter(
            models.Appointment.created_at >= week_ago
        ).scalar()
    }