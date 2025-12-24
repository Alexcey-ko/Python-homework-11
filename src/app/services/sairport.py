"""Функции для работы с аэропортами."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.sairport import SairportRepository


class SairportService:
    """Класс-сервис аэропортов."""
    def __init__(self, session: AsyncSession):
        """Инициализация сервиса."""
        self.session = session
        self.sairp_repo = SairportRepository(self.session)

    async def get_uniq_city_list(self) -> list[str]:
        """Получение списка всех городов."""
        sairp_repo = SairportRepository(self.session)
        return await sairp_repo.get_city_list_distinct()