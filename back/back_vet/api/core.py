from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()

origins = [
    "http://localhost:8080",             
    "https://clinicfastpig.netlify.app",      # ваш домен на Netlify
]
import os
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




from sqlalchemy.orm import Session
from database.session import SessionLocal
from database.models.user import User
from .utils.security import get_password_hash   # путь может отличаться

def create_admin_if_not_exists():
    db: Session = SessionLocal()
    try:
        # Проверяем, есть ли уже администратор
        admin = db.query(User).filter(User.role == "admin").first()
        if not admin:
            # Получаем данные администратора из переменных окружения
            admin_email = os.environ.get("ADMIN_EMAIL", "admin@fastpig.com")
            admin_phone = os.environ.get("ADMIN_PHONE", "+375291234567")
            admin_name = os.environ.get("ADMIN_NAME", "Главный администратор")
            admin_password = os.environ.get("ADMIN_PASSWORD", "Admin123!")

            # Хешируем пароль
            hashed_password = get_password_hash(admin_password)

            # Создаём пользователя с ролью admin
            new_admin = User(
                name=admin_name,
                phone=admin_phone,
                email=admin_email,
                password_hash=hashed_password,
                role="admin",
            )
            db.add(new_admin)
            db.commit()
            print("🔐 Администратор успешно создан!")
        else:
            print("✅ Администратор уже существует")
    except Exception as e:
        print(f"❌ Ошибка при создании администратора: {e}")
        db.rollback()
    finally:
        db.close()