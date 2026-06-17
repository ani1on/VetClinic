import os
import socket
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./vetclinic.db")

if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)

    # Supabase pooler может отдавать IPv6 — Render не поддерживает IPv6.
    # Резолвим хост в IPv4 и подставляем IP обратно в URL.
    try:
        from urllib.parse import urlparse, urlunparse
        parsed = urlparse(DATABASE_URL)
        hostname = parsed.hostname
        if hostname:
            ipv4 = socket.getaddrinfo(hostname, None, socket.AF_INET)[0][4][0]
            replaced = parsed._replace(netloc=parsed.netloc.replace(hostname, ipv4))
            DATABASE_URL = urlunparse(replaced)
    except Exception:
        pass

connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}

if "postgresql" in DATABASE_URL:
    connect_args["prepare_threshold"] = 0

engine = create_engine(DATABASE_URL, echo=False, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine)
