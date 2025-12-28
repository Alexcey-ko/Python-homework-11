"""Функции для работы с бронированием."""

from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from app.cache import cache
from app.exceptions import NotEnoughSeatsError
from app.repositories.sbook import SbookRepository
from app.schemas import SbookSchema
from app.schemas.sbook import SbookResponseSchema


class SbookService:
    """Класс-сервис бронирований."""
    def __init__(self, session: AsyncSession):
        """Инициализация сервиса."""
        self.session = session
        self.sbook_repo = SbookRepository(self.session, cache)

    async def get_sbooks(self):
        """Получение всех бронирований."""
        return await self.sbook_repo.get_sbooks()

    async def get_sbook_by_id(self, sbookid:int) -> SbookResponseSchema|None:
        """Получение бронирований с фильтрами."""
        return await self.sbook_repo.get_sbook_by_id(sbookid)

    async def get_sbooks_filtered(self, carrid:int|None = None, connid:int|None = None, fldate: date|None = None) -> list[SbookResponseSchema]:
        """Получение бронирований с фильтрами."""
        return await self.sbook_repo.get_sbooks_filtered(carrid, connid, fldate)
    
    async def book_flight(self, carrid:int, connid:int, fldate: date, scustom_id:int, seats:int) -> SbookSchema:
        """Бронирование выбранного рейса."""
        try:
            book = await self.sbook_repo.book_flight(carrid, connid, fldate, scustom_id, seats)
            return book
        except NotEnoughSeatsError as err:
            raise NotEnoughSeatsError from err
        
    async def delete_sbook(self, sbookid:int, scustom_id:int) -> SbookSchema|None:
        """Удаление бронирования."""
        return await self.sbook_repo.delete_sbook(sbookid, scustom_id)