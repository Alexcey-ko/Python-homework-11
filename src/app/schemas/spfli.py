"""Схемы для Spfli."""

from pydantic import BaseModel


class SpfliSchema(BaseModel):
    """Схема Spfli."""
    #Ключевые поля
    carrid: int
    connid: int
    #Вторичные поля
    airpfrom: int
    airpto: int
    fltime: int