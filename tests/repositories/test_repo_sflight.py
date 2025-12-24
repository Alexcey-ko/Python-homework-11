"""Модуль с тестами для репозитория рейсов."""

import pytest
from sqlalchemy import select

from app.models import Sflight
from app.repositories import SflightRepository
from tests.factories import SflightDataFactory


@pytest.fixture(autouse = True)
async def clean_sflight_counters():
    """Подготовка зависимых данных для Sflight."""
    SflightDataFactory.reset_fldate_set()

@pytest.mark.asyncio(loop_scope='session')
class TestSflightRepository:
    """Группа тестов репозитория клиентов."""

    async def test_sflight_create_single(self, db_session, spfli_data_list):
        """Проверка работы контейнера."""
        #Подготовка данных
        sflight_repo = SflightRepository(db_session)
        sflight_data = SflightDataFactory.build_with_refs(spfli_data_list)
        #Добавление и коммит данных в БД
        sflight_data_flush = await sflight_repo.create_sflight_single(sflight_data)
        await db_session.commit()

        #Выборка добавленной записи по ID
        sflight_query = select(Sflight).filter_by(carrid = sflight_data_flush.carrid, connid = sflight_data_flush.connid, fldate = sflight_data_flush.fldate)
        sflight_stmt = await db_session.execute(sflight_query)
        select_sflight = sflight_stmt.scalar_one_or_none()

        #Проверка, что маршрут был найден в БД
        assert select_sflight

    async def test_sflight_create_list(self, db_session, spfli_data_list):
        """Проверка работы контейнера."""
        #Подготовка данных
        sflight_repo = SflightRepository(db_session)
        sflight_list = SflightDataFactory.build_with_refs_batch(3, spfli_data_list)

        #Добавление и коммит данных в БД
        await sflight_repo.create_sflight_list(sflight_list)
        await db_session.commit()

        #Выборка всех маршрутов
        sflight_query = select(Sflight)
        sflight_stmt = await db_session.execute(sflight_query)
        select_sflight = sflight_stmt.scalars().all()

        #Проверка, что количество записей равно длине переданного списка
        assert len(select_sflight) == len(sflight_list)

    async def test_get_sflight_by_cities(self, db_session, sflight_routes_with_counts):
        """Проверка выборки рейсов из города отправления в город назначения."""
        #Подготовка данных
        sflight_repo = SflightRepository(db_session)

        for city_from, city_to, expected in sflight_routes_with_counts:
            #Выборка списка рейсов Sflight по городам
            assert len(await sflight_repo.get_sflight_by_cities(city_from, city_to)) == expected