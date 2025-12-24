"""Описание сущностей для Spfli."""

from pydantic import BaseModel


class SpfliData(BaseModel):
    """Тип данных для объектов Spfli."""
    #Ключевые поля
    carrid: int
    connid: int
    #Вторичные поля
    airpfrom: int
    airpto: int
    fltime: int