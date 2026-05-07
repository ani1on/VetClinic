from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import datamodels as schemas
from ..dependencies import get_db, get_current_admin
from ...database.crud.admin import get_dashboard

router = APIRouter(prefix="/api/admin", tags=["admin"])

@router.get("/dashboard", response_model=schemas.admin.DashboardMetricsResponse)
def dashboard(admin = Depends(get_current_admin), db: Session = Depends(get_db)):
    return get_dashboard(db)