from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models

def get_dashboard(db: Session) -> dict:
    now = datetime.utcnow()
    week_ago = now - timedelta(days=7)

    total_appointments = db.query(func.count(models.Appointment.id)).scalar()
    appointments_this_week = db.query(func.count(models.Appointment.id)) \
        .filter(models.Appointment.created_at >= week_ago).scalar()
    pending_appointments = db.query(func.count(models.Appointment.id)) \
        .filter(models.Appointment.status == "pending").scalar()

    total_users = db.query(func.count(models.User.id)).scalar()
    new_users_this_week = db.query(func.count(models.User.id)) \
        .filter(models.User.created_at >= week_ago).scalar()

    total_products = db.query(func.count(models.Product.id)).scalar()
    low_stock_products = db.query(func.count(models.Product.id)) \
        .filter(models.Product.stock_quantity <= 5, models.Product.is_available == True).scalar()

    pending_reviews = db.query(func.count(models.Review.id)) \
        .filter(models.Review.status == "pending").scalar()

    return {
        "total_appointments": total_appointments,
        "appointments_this_week": appointments_this_week,
        "pending_appointments": pending_appointments,
        "total_users": total_users,
        "new_users_this_week": new_users_this_week,
        "total_products": total_products,
        "low_stock_products": low_stock_products,
        "pending_reviews": pending_reviews,
    }