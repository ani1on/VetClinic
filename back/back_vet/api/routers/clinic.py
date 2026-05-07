from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import datamodels as schemas
from ..dependencies import get_db, get_current_admin
from ...database.crud.clinic import get_info, update_info

router = APIRouter(prefix="/api/clinic", tags=["clinic"])

@router.get("/about", response_model=schemas.clinic.ClinicInfoResponse)
def about(db: Session = Depends(get_db)):
    info = get_info(db)
    if not info:
        raise HTTPException(status_code=404, detail="Информация не заполнена")
    return info

@router.put("/admin/clinic/about", response_model=schemas.clinic.ClinicInfoResponse)
def update_about(payload: schemas.clinic.ClinicInfoUpdateRequest, admin = Depends(get_current_admin), db: Session = Depends(get_db)):
    return update_info(db, payload.dict(exclude_unset=True))