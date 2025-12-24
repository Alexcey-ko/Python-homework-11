"""Модуль с тестами для репозитория аэропортов."""

import pytest
from sqlalchemy import select

from app.models import Sairport
from app.repositories import SairportRepository
from tests.factories import SairportDataFactory


@pytest.mark.asyncio(loop_scope='session')
class TestSairportRepository:
    """Группа тестов репозитория аэропортов."""
    
    async def test_airport_create_single(self, db_session):
        """Проверка работы контейнера."""
        #Подготовка данных
        airport_repo = SairportRepository(db_session)
        airp_data = SairportDataFactory()
        #Добавление и коммит данных в БД
        airp_data_flush = await airport_repo.create_sairport_single(airp_data)
        await db_session.commit()

        #Выборка добавленной записи по ID
        airp_query = select(Sairport).filter_by(id = airp_data_flush.id)
        airp_stmt = await db_session.execute(airp_query)
        select_airport = airp_stmt.scalar_one_or_none()

        #Проверка, что аэропорт был найден в БД
        assert select_airport

    async def test_airport_create_list(self, db_session):
        """Проверка работы контейнера."""
        #Подготовка данных
        airport_repo = SairportRepository(db_session)
        airport_list = SairportDataFactory.build_batch(3)

        #Добавление и коммит данных в БД
        await airport_repo.create_sairport_list(airport_list)
        await db_session.commit()

        #Выборка всех аэропортов
        airp_query = select(Sairport)
        airp_stmt = await db_session.execute(airp_query)
        select_airport = airp_stmt.scalars().all()

        #Проверка, что количество записей равно длине переданного списка
        assert len(select_airport) == len(airport_list)

    async def test_get_unique_cities(self, db_session):
        """Проверка выбора уникальных городов."""
        #Подготовка данных
        airport_repo = SairportRepository(db_session)
        city_count = 5
        #Создание списка аэропортов по 3 на каждый уникальный город
        airport_list = [
            airport
            for i in range(city_count)
            for airport in SairportDataFactory.build_batch(3, city=f'Город №{i}') ]
        await airport_repo.create_sairport_list(airport_list)
        await db_session.commit()

        #Выборка уникальных городов
        unique_cities = await airport_repo.get_city_list_distinct()

        #Проверка, что количество выбранных городов равно заданному
        assert len(unique_cities) == city_count