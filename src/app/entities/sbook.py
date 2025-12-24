"""Описание сущностей для Sbook."""

from datetime import date

from pydantic import BaseModel


class SbookData(BaseModel):
    """Тип данных для объектов Sbook."""
    #Ключевые поля
    carrid: int
    connid: int
    fldate: date
    bookid: int
    #Вторичные поля
    customid: int
    seats: int