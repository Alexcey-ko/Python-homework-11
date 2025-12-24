"""Описание сущностей для Sairport."""

from pydantic import BaseModel


class SairportData(BaseModel):
    """Тип данных для объектов Sairport."""
    #Ключевые поля
    id: int|None = None
    #Неключевые поля
    name: str
    timezone: str
    country: str
    city: str