"""Схемы для Scarr."""

from pydantic import BaseModel


class ScarrSchema(BaseModel):
    """Схема Scarr."""
    #Ключевые поля
    carrid: int|None = None
    #Вторичные поля
    carrname: str
    carrcode: str
    url: str