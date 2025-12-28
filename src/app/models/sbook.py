"""Таблица бронирований SBOOK."""

from datetime import date

from sqlalchemy import Date, ForeignKey, ForeignKeyConstraint, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Sbook(Base):
    """Класс представляющий таблицу БД SBOOK."""
    __tablename__ = 'sbook'
    #Ключевые поля
    sbookid: Mapped[int] = mapped_column(Integer, primary_key=True)
    #Вторичные поля
    carrid: Mapped[int] = mapped_column(Integer, ForeignKey('scarr.carrid'))
    connid: Mapped[int] = mapped_column(Integer)
    fldate: Mapped[date] = mapped_column(Date)
    bookid: Mapped[int] = mapped_column(Integer)
    customid: Mapped[int] = mapped_column(Integer, ForeignKey('scustom.id'))
    seats: Mapped[int] = mapped_column(Integer, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(
            ['carrid', 'connid', 'fldate'],
            ['sflight.carrid', 'sflight.connid', 'sflight.fldate']
        ),
    )