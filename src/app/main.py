"""Приложение для бронирования авиабилетов."""

from fastapi import FastAPI

from app.auth import security
from app.routers import main_router

app = FastAPI(title = 'Booking API')
app.include_router(main_router)
security.handle_errors(app)