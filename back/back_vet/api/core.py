import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ..database.core import SessionLocal, init_db
from ..database.models.user import User
from .utils.security import get_password_hash

app = FastAPI()

origins = [
    "http://localhost:8080",
    "https://clinicfastpig.netlify.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def create_admin_if_not_exists():
    init_db()

    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.role == "admin").first()
        if not admin:
            admin_email = os.environ.get("ADMIN_EMAIL", "admin@fastpig.com")
            admin_phone = os.environ.get("ADMIN_PHONE", "+375291234567")
            admin_name = os.environ.get("ADMIN_NAME", "Главный администратор")
            admin_password = os.environ.get("ADMIN_PASSWORD", "Admin123!")

            hashed = get_password_hash(admin_password)

            new_admin = User(
                name=admin_name,
                phone=admin_phone,
                email=admin_email,
                password_hash=hashed,
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
