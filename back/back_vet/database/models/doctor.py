from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Time
from sqlalchemy.orm import relationship

from .base import Base


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    full_name = Column(String(150), nullable=False)
    specialization = Column(String(200))
    description = Column(String)
    photo_url = Column(String(300))
    is_active = Column(Boolean, default=True)

    user = relationship("User")
    schedules = relationship("DoctorSchedule", back_populates="doctor")
    appointments = relationship("Appointment", back_populates="doctor")
    medical_records = relationship("MedicalRecord", back_populates="doctor")


class DoctorSchedule(Base):
    __tablename__ = "doctor_schedules"

    id = Column(Integer, primary_key=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id", ondelete="CASCADE"))
    work_date = Column(Date)
    start_time = Column(Time)
    end_time = Column(Time)
    slot_duration = Column(Integer, default=30)
    is_available = Column(Boolean, default=True)

    doctor = relationship("Doctor", back_populates="schedules")