"""Схемы для Sbook."""
from datetime import date
from decimal import Decimal
from typing import Annotated, Optional

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
    sbookid: Annotated[Optional[int], Field(..., description = 'ID бронирования')] = None
    #Вторичные поля
    carrname: Annotated[str, Field(..., description = 'Наименование компании перевозчика')]
    cityfrom: Annotated[str, Field(..., description = 'Город отправления')]
    airpfrom: Annotated[int, Field(..., description = 'ID аэропорта отправления')]
    cityto: Annotated[str, Field(..., description = 'Город назначения')]
    airpto: Annotated[int, Field(..., description = 'ID аэропорта назначения')]
    fltime: Annotated[int, Field(..., description = 'Время полета в секундах')]
    price: Annotated[Decimal, Field(..., description = 'Стоимость билета не рейс')]
    currency: Annotated[str, Field(..., description = 'Валюта')]

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