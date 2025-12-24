"""Таблица рейсов SAIRPORT."""

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Sairport(Base):
    """Класс представляющий таблицу БД SAIRPORT."""
    __tablename__ = 'sairport'
    #Ключевые поля
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    #Вторичные поля
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    timezone: Mapped[str] = mapped_column(String(50), nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False, index=True)