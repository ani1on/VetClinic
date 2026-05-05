from sqlalchemy import Column, Integer, Date, Time, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from .base import Base


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    pet_id = Column(Integer, ForeignKey("pets.id"))
    service_id = Column(Integer, ForeignKey("services.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    appointment_date = Column(Date)
    appointment_time = Column(Time)
    comment = Column(Text)
    status = Column(String(20), default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="appointments")
    pet = relationship("Pet", back_populates="appointments")
    service = relationship("Service", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")