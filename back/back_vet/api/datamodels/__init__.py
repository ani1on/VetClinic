from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import date, time, datetime

class ORMModel(BaseModel):
    class Config:
        from_attributes = True

from . import auth
from . import user
from . import admin
from . import appointment
from . import cart
from . import clinic
from . import doctor
from . import favorite
from . import news
from . import order
from . import pet
from . import product
from . import review
from . import service