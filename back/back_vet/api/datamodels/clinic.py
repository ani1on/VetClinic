from pydantic import Field, BaseModel
from typing import Optional
from . import ORMModel

class ClinicInfoUpdateRequest(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    working_hours: Optional[str] = None   # JSON строка
    social_links: Optional[str] = None
    licenses: Optional[str] = None
    about_text: Optional[str] = None

class ClinicInfoResponse(ORMModel):
    id: int
    name: str
    address: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    working_hours: Optional[str]
    social_links: Optional[str]
    licenses: Optional[str]
    about_text: Optional[str]
