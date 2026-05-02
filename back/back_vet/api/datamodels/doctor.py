from pydantic import Field
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
    # можно добавить расписание
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