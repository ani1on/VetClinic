from sqlalchemy import Column, Integer, String, Text

from .base import Base


class ClinicInfo(Base):
    __tablename__ = "clinic_info"

    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    address = Column(Text)
    phone = Column(String(50))
    email = Column(String(100))
    working_hours = Column(Text)
    social_links = Column(Text)
    licenses = Column(Text)
    about_text = Column(Text)