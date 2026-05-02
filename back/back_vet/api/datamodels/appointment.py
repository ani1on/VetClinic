from pydantic import Field, validator
from typing import Optional
from datetime import date, time, datetime
from . import ORMModel
from .service import ServiceResponse
from .doctor import DoctorResponse

class AppointmentCreateRequest(BaseModel):
    pet_id: int
    service_id: int
    doctor_id: Optional[int] = None
    appointment_date: date
    appointment_time: time
    comment: Optional[str] = None

class AppointmentUpdateRequest(BaseModel):
    appointment_date: Optional[date] = None
    appointment_time: Optional[time] = None
    comment: Optional[str] = None

class AppointmentStatusUpdate(BaseModel):
    status: str = Field(..., regex='^(pending|confirmed|canceled|completed|paid)$')

class AppointmentResponse(ORMModel):
    id: int
    user_id: int
    pet_id: int
    service_id: int
    doctor_id: Optional[int]
    appointment_date: date
    appointment_time: time
    comment: Optional[str]
    status: str
    created_at: datetime
    # связанные объекты (можно возвращать по желанию)
    service: Optional[ServiceResponse] = None
    doctor: Optional[DoctorResponse] = None
    # pet? не перегружаем, но можно

class AppointmentListResponse(ORMModel):
    total: int
    appointments: list[AppointmentResponse]
