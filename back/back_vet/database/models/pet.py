from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Boolean, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from .base import Base


class Pet(Base):
    __tablename__ = "pets"

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    name = Column(String(50), nullable=False)
    species = Column(String(50))
    breed = Column(String(100))
    gender = Column(String(10))
    birth_date = Column(Date)
    weight = Column(Float)
    color = Column(String(50))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_archived = Column(Boolean, default=False)

    owner = relationship("User", back_populates="pets")
    medical_records = relationship("MedicalRecord", back_populates="pet")
    appointments = relationship("Appointment", back_populates="pet")


class MedicalRecord(Base):
    __tablename__ = "pet_medical_history"

    id = Column(Integer, primary_key=True)
    pet_id = Column(Integer, ForeignKey("pets.id", ondelete="CASCADE"))
    visit_date = Column(DateTime, default=datetime.utcnow)
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    diagnosis = Column(Text)
    treatment = Column(Text)
    notes = Column(Text)
    files = Column(JSON)

    pet = relationship("Pet", back_populates="medical_records")
    doctor = relationship("Doctor", back_populates="medical_records")