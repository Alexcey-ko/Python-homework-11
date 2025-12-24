"""Функции для работы с рейсами."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.cache import cache
from app.entities import SflightData
from app.repositories.sflight import SflightRepository


class SflightService:
    """Класс-сервис аэропортов."""
    def __init__(self, session: AsyncSession):
        """Инициализация сервиса."""
        self.session = session
        self.sflight_repo = SflightRepository(self.session, cache)

    async def get_sflights(self, from_city:str, to_city:str)->list[SflightData]:
        """Получение рейсов по городам отправления -> назначения."""
        return await self.sflight_repo.get_sflight_by_cities(from_city, to_city)