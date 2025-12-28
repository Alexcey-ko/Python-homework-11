"""Базовый класс репозитория."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.cache import Cache
from app.database import async_session


class Repository():
    """Базовый клсс для классов Repository."""

    def __init__(self, session: AsyncSession|None, cache: Cache | None = None):
        """Инициализация объекта."""
        if session is None:
            self.session = async_session()
        else:
            self.session = session
        self.cache = cache