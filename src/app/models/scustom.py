"""Таблица клиентов SCUSTOM."""

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Scustom(Base):
    """Класс представляющий таблицу БД SCUSTOM."""
    __tablename__ = 'scustom'
    #Ключевые поля
    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True, autoincrement=True)
    #Вторичные поля
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=False)
    name: Mapped[str | None] = mapped_column(String(50), nullable=False)