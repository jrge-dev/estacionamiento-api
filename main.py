from app.routes import ticket_routes, auth_routes, car_routes
from fastapi import FastAPI

app = FastAPI()


app.include_router(ticket_routes.router)
app.include_router(auth_routes.router)
app.include_router(car_routes.router)
