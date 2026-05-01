from pydantic import Field, BaseModel
from typing import Optional, List
from datetime import date, datetime
from . import ORMModel

class PetCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    species: str = Field(..., max_length=50)
    breed: Optional[str] = None
    gender: Optional[str] = None
    birth_date: Optional[date] = None
    weight: Optional[float] = None
    color: Optional[str] = None
    notes: Optional[str] = None

class PetUpdateRequest(BaseModel):
    name: Optional[str] = None
    species: Optional[str] = None
    breed: Optional[str] = None
    gender: Optional[str] = None
    birth_date: Optional[date] = None
    weight: Optional[float] = None
    color: Optional[str] = None
    notes: Optional[str] = None

class MedicalRecordResponse(ORMModel):
    id: int
    pet_id: int
    visit_date: datetime
    doctor_id: Optional[int]
    diagnosis: Optional[str]
    treatment: Optional[str]
    notes: Optional[str]
    files: Optional[str]   # строка с JSON или CSV

class PetResponse(ORMModel):
    id: int
    owner_id: int
    name: str
    species: str
    breed: Optional[str]
    gender: Optional[str]
    birth_date: Optional[date]
    weight: Optional[float]
    color: Optional[str]
    notes: Optional[str]
    created_at: datetime
    is_archived: bool
    # Медицинская история опционально
    medical_records: Optional[List[MedicalRecordResponse]] = []