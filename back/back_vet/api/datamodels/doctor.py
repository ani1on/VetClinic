from pydantic import Field, BaseModel
from typing import Optional, List
from datetime import date, time
from . import ORMModel

class DoctorResponse(ORMModel):
    id: int
    full_name: str
    specialization: Optional[str]
    description: Optional[str]
    photo_url: Optional[str]
    is_active: bool

class DoctorDetailResponse(DoctorResponse):

    schedules: Optional[List['DoctorScheduleResponse']] = []

class DoctorScheduleResponse(ORMModel):
    id: int
    doctor_id: int
    work_date: date
    start_time: time
    end_time: time
    slot_duration: int
    is_available: bool

class SlotResponse(ORMModel):
    time: time
    available: bool


class DoctorCreateRequest(BaseModel):
    user_id: int = Field(..., description="ID пользователя")
    full_name: str = Field(..., max_length=150)
    specialization: Optional[str] = None
    description: Optional[str] = None
    photo_url: Optional[str] = None
    is_active: bool = True

class DoctorUpdateRequest(BaseModel):
    full_name: Optional[str] = None
    specialization: Optional[str] = None
    description: Optional[str] = None
    photo_url: Optional[str] = None
    is_active: Optional[bool] = None