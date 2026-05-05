from sqlalchemy import Column, Integer, String, Float, Boolean, Text
from sqlalchemy.orm import relationship

from .base import Base


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    duration_minutes = Column(Integer, default=30)
    category = Column(String(100))
    is_active = Column(Boolean, default=True)

    appointments = relationship("Appointment", back_populates="service")