"""Модуль для работы с БД."""

from sqlalchemy import URL
from sqlalchemy.ext import asyncio as sa_async
from sqlalchemy.orm import DeclarativeBase, declarative_base, sessionmaker

from app.config import config


def get_db_url(dialect:str = 'postgresql', driver:str = 'asyncpg')->URL:
    """Формирование URL для подключения к БД."""
    return URL.create(
        f'{dialect}+{driver}',
        username = config.POSTGRES_USER,
        password = config.POSTGRES_PASSWORD,
        host = config.POSTGRES_HOST,
        port = config.POSTGRES_PORT,
        database = config.POSTGRES_DB )

def get_async_engine():
    """Создание асинхронного движка для работы с БД."""
    return sa_async.create_async_engine(
        url = get_db_url(),
        #echo=True,
    )

#Движок для работы с БД
engine: sa_async.AsyncEngine = get_async_engine()

#Фабрику сессий
async_session:sa_async.async_sessionmaker[sa_async.AsyncSession] = sessionmaker(
    engine, 
    expire_on_commit = False, 
    class_ = sa_async.AsyncSession)

#Базовый класс для создания таблиц БД
Base:DeclarativeBase = declarative_base()