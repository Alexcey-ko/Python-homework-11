"""Модуль с тестами для репозитория клиентов."""

import pytest
from sqlalchemy import select

from app.models import Spfli
from app.repositories import SpfliRepository
from tests.factories import SpfliDataFactory


@pytest.fixture(autouse = True)
async def clean_spfli_counters():
    """Подготовка зависимых данных для Spfli."""
    SpfliDataFactory.reset_counters()

@pytest.mark.asyncio(loop_scope='session')
class TestSpfliRepository:
    """Группа тестов репозитория клиентов."""

    async def test_spfli_create_single(self, db_session, scarr_data_list, sairport_data_list):
        """Проверка работы контейнера."""
        #Подготовка данных
        spfli_repo = SpfliRepository(db_session)
        spfli_data = SpfliDataFactory.build_with_refs(scarr_data_list, sairport_data_list)
        #Добавление и коммит данных в БД
        spfli_data_flush = await spfli_repo.create_spfli_single(spfli_data)
        await db_session.commit()

        #Выборка добавленной записи по ID
        spfli_query = select(Spfli).filter_by(carrid = spfli_data_flush.carrid, connid = spfli_data_flush.connid)
        spfli_stmt = await db_session.execute(spfli_query)
        select_spfli = spfli_stmt.scalar_one_or_none()

        #Проверка, что маршрут был найден в БД
        assert select_spfli

    async def test_spfli_create_list(self, db_session, scarr_data_list, sairport_data_list):
        """Проверка работы контейнера."""
        #Подготовка данных
        spfli_repo = SpfliRepository(db_session)
        spfli_list = SpfliDataFactory.build_with_refs_batch(3, scarr_data_list, sairport_data_list)

        #Добавление и коммит данных в БД
        await spfli_repo.create_spfli_list(spfli_list)
        await db_session.commit()

        #Выборка всех маршрутов
        spfli_query = select(Spfli)
        spfli_stmt = await db_session.execute(spfli_query)
        select_spfli = spfli_stmt.scalars().all()

        #Проверка, что количество записей равно длине переданного списка
        assert len(select_spfli) == len(spfli_list)
