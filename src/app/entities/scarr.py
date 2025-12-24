"""Описание сущностей для Scarr."""

from pydantic import BaseModel


class ScarrData(BaseModel):
    """Тип данных для объектов Scarr."""
    #Ключевые поля
    carrid: int|None = None
    #Вторичные поля
    carrname: str
    carrcode: str
    url: str