from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .core import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default="client")  # client, doctor, admin
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    #todo: добавить отношения