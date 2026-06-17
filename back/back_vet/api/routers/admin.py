from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from .. import datamodels as schemas
from ..dependencies import get_db, get_current_admin
from ...database.crud.admin import get_dashboard
from ...database.models.user import User

router = APIRouter(prefix="/api/admin", tags=["admin"])

@router.get("/dashboard", response_model=schemas.admin.DashboardMetricsResponse)
def dashboard(admin = Depends(get_current_admin), db: Session = Depends(get_db)):
    return get_dashboard(db)

@router.get("/utm-stats")
def utm_stats(admin = Depends(get_current_admin), db: Session = Depends(get_db)):
    sources = db.query(
        User.utm_source, func.count(User.id)
    ).filter(User.utm_source.isnot(None)).group_by(User.utm_source).all()

    mediums = db.query(
        User.utm_medium, func.count(User.id)
    ).filter(User.utm_medium.isnot(None)).group_by(User.utm_medium).all()

    campaigns = db.query(
        User.utm_campaign, func.count(User.id)
    ).filter(User.utm_campaign.isnot(None)).group_by(User.utm_campaign).all()

    total_with_utm = db.query(func.count(User.id)).filter(User.utm_source.isnot(None)).scalar()
    total_users = db.query(func.count(User.id)).scalar()

    return {
        "total_users": total_users,
        "total_with_utm": total_with_utm,
        "by_source": [{"source": s, "count": c} for s, c in sources],
        "by_medium": [{"medium": m, "count": c} for m, c in mediums],
        "by_campaign": [{"campaign": c, "count": n} for c, n in campaigns],
    }