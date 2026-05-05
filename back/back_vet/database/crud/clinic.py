from sqlalchemy.orm import Session
from .. import models
from .base import safe_commit


def get_info(db: Session):
    return db.query(models.ClinicInfo).first()


def update_info(db: Session, payload: dict):
    info = get_info(db)

    if not info:
        info = models.ClinicInfo(**payload)
        db.add(info)
    else:
        for k, v in payload.items():
            if hasattr(info, k):
                setattr(info, k, v)

    safe_commit(db)
    db.refresh(info)
    return info