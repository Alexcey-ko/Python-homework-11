"""Таблица рейсов SPFLI."""

from sqlalchemy import ForeignKey, Index, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models import Sairport, Scarr


class Spfli(Base):
    """Класс представляющий таблицу БД SPFLI."""
    __tablename__ = 'spfli'
    #Ключевые поля
    carrid: Mapped[int] = mapped_column(Integer, ForeignKey('scarr.carrid'), primary_key=True)
    connid: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    #Вторичные поля
    airpfrom: Mapped[int] = mapped_column(Integer, ForeignKey('sairport.id'), nullable=False)
    airpto: Mapped[int] = mapped_column(Integer, ForeignKey('sairport.id'), nullable=False)
    fltime: Mapped[int] = mapped_column(Integer, nullable=False)
    
    scarr: Mapped['Scarr'] = relationship('Scarr')
    sairportfrom: Mapped['Sairport'] = relationship('Sairport', foreign_keys=[airpfrom])
    sairportto: Mapped['Sairport']  = relationship('Sairport', foreign_keys=[airpto])

    __table_args__ = (
        Index('idx_spfli_from_to', 'airpfrom', 'airpto'),
    )