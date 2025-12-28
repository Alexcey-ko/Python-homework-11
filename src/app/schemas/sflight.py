"""Схемы для Sflight."""

from datetime import date
from decimal import Decimal

from pydantic import BaseModel


class SflightSchema(BaseModel):
    """Схема Sflight."""
    #Ключевые поля
    carrid: int
    connid: int
    fldate: date
    #Вторичные поля
    price: Decimal
    currency: str
    planetype: str
    seatsmax: int
    seatsocc: int
    av_seats: int