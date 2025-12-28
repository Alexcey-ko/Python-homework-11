"""Схемы для Sairport."""

from pydantic import BaseModel


class SairportSchema(BaseModel):
    """Схема Sairport."""
    #Ключевые поля
    id: int|None = None
    #Неключевые поля
    name: str
    timezone: str
    country: str
    city: str