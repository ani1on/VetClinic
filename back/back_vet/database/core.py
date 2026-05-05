from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

# Импортируем Base из ваших моделей
from .models import Base

DATABASE_URL = "sqlite:///./vetclinic.db"

# Аргумент connect_args нужен только для SQLite
engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    # Этот вызов создаст все таблицы, которые наследуются от Base
    Base.metadata.create_all(bind=engine)