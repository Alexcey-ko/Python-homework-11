"""Функции для работы с бронированием."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.cache import cache
from app.entities import ScustomAuth, SflightData
from app.exceptions import NotEnoughSeatsError
from app.repositories.sbook import SbookRepository


class SbookService:
    """Класс-сервис бронирований."""
    def __init__(self, session: AsyncSession):
        """Инициализация сервиса."""
        self.session = session
        self.sbook_repo = SbookRepository(self.session, cache)

    async def book_flight(self, sfl:SflightData, scust:ScustomAuth, seats:int) -> bool:
        """Бронирование выбранного рейса."""
        try:
            book = await self.sbook_repo.book_flight(sfl, scust, seats)
            return bool(book)
        except NotEnoughSeatsError as err:
            raise NotEnoughSeatsError from err