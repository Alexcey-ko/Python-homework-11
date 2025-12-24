"""CONFTEST."""

import pytest
from sqlalchemy import text
from sqlalchemy.ext import asyncio as sa_async
from testcontainers.postgres import PostgresContainer
from testcontainers.redis import RedisContainer

from app.database import Base


@pytest.fixture(scope='session')
def postgres_container():
    """Создание тестового POSTGRES контейнера."""
    with PostgresContainer(
        image = 'postgres:alpine',
        username = 'test_user',
        password = 'test_password',  # noqa: S106
        dbname = 'test_db',
        driver = 'asyncpg',
    ) as postgres:
        yield postgres

@pytest.fixture(scope='session')
async def async_engine(postgres_container):
    """Создание тествого джвика для POSTGRES."""
    engine: sa_async.AsyncEngine = sa_async.create_async_engine(postgres_container.get_connection_url())
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()

@pytest.fixture(scope='session')
def async_session_factory(async_engine):
    """Создание фабрики сессий для POSTGRES."""
    return sa_async.async_sessionmaker(
        bind = async_engine,
        expire_on_commit =False,
        class_ = sa_async.AsyncSession )

@pytest.fixture
async def db_session(async_session_factory):
    """Создание сессии для POSTGRES."""
    async with async_session_factory() as session:
        yield session
        await session.rollback()

@pytest.fixture(autouse=True)
async def clean_db(async_engine):
    """Очистка таблиц БД перед каждым тестом."""
    async with async_engine.begin() as conn:
        await conn.execute(
            text(
                """
                DO $$
                DECLARE
                    r RECORD;
                BEGIN
                    FOR r IN (
                        SELECT tablename
                        FROM pg_tables
                        WHERE schemaname = 'public'
                    ) LOOP
                        EXECUTE 'TRUNCATE TABLE ' || quote_ident(r.tablename) || ' RESTART IDENTITY CASCADE';
                    END LOOP;
                END
                $$;
                """
            )
        )

@pytest.fixture(scope='session')
def redis_container():
    """Создание тестового REDIS контейнера."""
    with RedisContainer() as redis:
        yield redis