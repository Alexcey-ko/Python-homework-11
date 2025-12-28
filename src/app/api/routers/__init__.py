from fastapi import APIRouter

from app.api.routers.auth import router as auth_router
from app.api.routers.booking import router as sbook_router

main_router = APIRouter()

main_router.include_router(auth_router, tags = ['Аутентификация'])
main_router.include_router(sbook_router, tags = ['Бронирование'])