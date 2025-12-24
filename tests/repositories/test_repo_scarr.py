"""Модуль с тестами для репозитория клиентов."""

import pytest
from sqlalchemy import select

from app.models import Scarr
from app.repositories import ScarrRepository
from tests.factories import ScarrDataFactory


@pytest.mark.asyncio(loop_scope='session')
class TestScarrRepository:
    """Группа тестов репозитория клиентов."""

    async def test_scarr_create_single(self, db_session):
        """Проверка работы контейнера."""
        #Подготовка данных
        scarr_repo = ScarrRepository(db_session)
        scarr_data = ScarrDataFactory()
        #Добавление и коммит данных в БД
        scarr_data_flush = await scarr_repo.create_scarr_single(scarr_data)
        await db_session.commit()

        #Выборка добавленной записи по ID
        scarr_query = select(Scarr).filter_by(carrid = scarr_data_flush.carrid)
        scarr_stmt = await db_session.execute(scarr_query)
        select_scarr = scarr_stmt.scalar_one_or_none()

        #Проверка, что аэропорт был найден в БД
        assert select_scarr

    async def test_scarr_create_list(self, db_session):
        """Проверка работы контейнера."""
        #Подготовка данных
        scarr_repo = ScarrRepository(db_session)
        scarr_list = ScarrDataFactory.build_batch(3)

        #Добавление и коммит данных в БД
        await scarr_repo.create_scarr_list(scarr_list)
        await db_session.commit()

        #Выборка всех аэропортов
        scarr_query = select(Scarr)
        scarr_stmt = await db_session.execute(scarr_query)
        select_scarr = scarr_stmt.scalars().all()

        #Проверка, что количество записей равно длине переданного списка
        assert len(select_scarr) == len(scarr_list)