from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

from .models import Base

DATABASE_URL = "sqlite:///./vetclinic.db"

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
    Base.metadata.create_all(bind=engine)

def set_first_admin():
    db = SessionLocal()
    # Найдите пользователя по email или phone (укажите нужные данные)
    admin_user = db.query(User).filter(User.email == "anilon5656@gmail.com").first()
    if admin_user and admin_user.role != "admin":
        admin_user.role = "admin"
        db.commit()
        print("Администратор назначен!")
    db.close()