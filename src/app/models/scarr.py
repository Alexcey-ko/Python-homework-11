"""Таблица перевозчиков SCARR."""

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Scarr(Base):
    """Класс представляющий таблицу БД SCARR."""
    __tablename__ = 'scarr'
    #Ключевые поля
    carrid: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    #Вторичные поля
    carrname: Mapped[str] = mapped_column(String(100), nullable=False)
    carrcode: Mapped[str] = mapped_column(String(10), nullable=False)
    url: Mapped[str] = mapped_column(String(100), nullable=False)

