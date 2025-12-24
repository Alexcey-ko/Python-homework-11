"""Базовый класс репозитория."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.cache import Cache


class Repository():
    """Базовый клсс для классов Repository."""

    def __init__(self, session: AsyncSession|None, cache: Cache | None = None):
        """Инициализация объекта."""
        self.session = session
        self.cache = cache