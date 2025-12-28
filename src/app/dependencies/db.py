"""Зависимости БД."""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session


async def get_async_session():
    """Зависимость для сессии."""
    async with async_session() as session:
        yield session

AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]