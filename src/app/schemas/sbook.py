"""Схемы для SCUSTOM."""
from datetime import date
from decimal import Decimal

from pydantic import BaseModel


class SbookResponseSchema(BaseModel):
    """Схема для ответа на запрос Sbook."""
    #Ключевые поля
    carrid: int
    connid: int
    fldate: date
    bookid: int
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
    carrid: int
    connid: int
    fldate: date
    bookid: int
    #Вторичные поля
    customid: int
    seats: int