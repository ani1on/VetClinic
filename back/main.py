from .back_vet.api.core import app
from .back_vet.api.routers import auth, users

app.include_router(auth.router)
app.include_router(users.router)

@app.on_event("startup")
def startup():
    from .back_vet.database.core import init_db
    init_db()                       # ← создаёт все таблицы