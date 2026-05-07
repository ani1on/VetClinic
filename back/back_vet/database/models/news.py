from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from datetime import datetime

from .base import Base


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    content = Column(Text)
    image_url = Column(String(300))
    is_published = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime)