from .back_vet.api.core import app
from .back_vet.api.routers import (
    auth, users, pets, doctors, services, appointments,
    products, cart, orders, favorites, news, reviews, clinic, admin, token
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(pets.router)
app.include_router(doctors.router)
app.include_router(services.router)
app.include_router(appointments.router)
app.include_router(products.router)
app.include_router(cart.router)
app.include_router(orders.router)
app.include_router(favorites.router)
app.include_router(news.router)
app.include_router(reviews.router)
app.include_router(clinic.router)
app.include_router(admin.router)
app.include_router(token.router)
@app.on_event("startup")
def startup():
    from .back_vet.database.core import init_db
    init_db()
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)