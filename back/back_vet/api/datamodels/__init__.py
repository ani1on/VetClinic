from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import date, time, datetime

class ORMModel(BaseModel):
    class Config:
        from_attributes = True