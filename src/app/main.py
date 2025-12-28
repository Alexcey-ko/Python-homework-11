"""Приложение для бронирования авиабилетов."""

from fastapi import FastAPI

from app.api.routers import main_router
from app.auth import security

app = FastAPI(title = 'Booking API')
app.include_router(main_router)
security.handle_errors(app)