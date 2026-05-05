from sqlalchemy.orm import Session

def safe_commit(db: Session):
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise