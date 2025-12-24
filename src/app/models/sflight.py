"""Таблица вылетов SFLIGHT."""

from datetime import date
from decimal import Decimal

from sqlalchemy import Date, ForeignKey, ForeignKeyConstraint, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Sflight(Base):
    """Класс представляющий таблицу БД SFLIGHT."""
    __tablename__ = 'sflight'
    #Ключевые поля
    carrid: Mapped[int] = mapped_column(Integer, ForeignKey('scarr.carrid'), primary_key=True)
    connid: Mapped[int] = mapped_column(Integer, primary_key=True)
    fldate: Mapped[date] = mapped_column(Date, primary_key=True)
    #Вторичные поля
    price: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    planetype: Mapped[str] = mapped_column(String(30), nullable=False)
    seatsmax: Mapped[int] = mapped_column(Integer, nullable=False)
    seatsocc: Mapped[int] = mapped_column(Integer, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(
            ['carrid', 'connid'],
            ['spfli.carrid', 'spfli.connid']
        ),
    )