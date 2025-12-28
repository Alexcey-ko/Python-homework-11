"""Схемы для SBOOK."""
from datetime import date
from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, Field


class BookingSchema(BaseModel):
    """Схема рейса для бронирования."""
    carrid: Annotated[int, Field(..., description = 'ID перевозчика')]
    connid: Annotated[int, Field(..., description = 'ID маршрута')]
    fldate: Annotated[date, Field(..., description = 'Дата рейса')]
    seats: Annotated[int, Field(..., description = 'Количество мест для бронирования')] = 1

class SbookResponseSchema(BaseModel):
    """Схема для ответа на запрос Sbook."""
    #Ключевые поля
    sbookid: int|None = None
    #Вторичные поля
    carrname: str
    cityfrom: str
    airpfrom: int
    cityto: str
    airpto: int
    fltime: int
    price: Decimal
    currency: str

class SbookSchema(BaseModel):
    """Схема Sbook."""
    #Ключевые поля
    sbookid: int|None = None
    #Вторичные поля
    carrid: int
    connid: int
    fldate: date
    bookid: int
    customid: int
    seats: int