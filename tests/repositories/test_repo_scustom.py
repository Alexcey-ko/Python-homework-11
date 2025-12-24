"""Модуль с тестами для репозитория клиентов."""

import pytest
from sqlalchemy import select

from app.exceptions import UserAlreadyExistsError
from app.models import Scustom
from app.repositories import ScustomRepository
from tests.factories import ScustomDataFactory


@pytest.mark.asyncio(loop_scope='session')
class TestScustomRepository:
    """Группа тестов репозитория клиентов."""

    async def test_scustom_create_single(self, db_session):
        """Проверка работы контейнера."""
        #Подготовка данных
        scustom_repo = ScustomRepository(db_session)
        scust_data = ScustomDataFactory()
        #Добавление и коммит данных в БД
        scust_data_flush = await scustom_repo.create_scustom_single(scust_data)
        await db_session.commit()

        #Выборка добавленной записи по ID
        scust_query = select(Scustom).filter_by(id = scust_data_flush.id)
        scust_stmt = await db_session.execute(scust_query)
        select_scustom = scust_stmt.scalar_one_or_none()

        #Проверка, что аэропорт был найден в БД
        assert select_scustom

    async def test_scustom_create_list(self, db_session):
        """Проверка работы контейнера."""
        #Подготовка данных
        scustom_repo = ScustomRepository(db_session)
        scustom_list = ScustomDataFactory.build_batch(3)

        #Добавление и коммит данных в БД
        await scustom_repo.create_scustom_list(scustom_list)
        await db_session.commit()

        #Выборка всех аэропортов
        scust_query = select(Scustom)
        scust_stmt = await db_session.execute(scust_query)
        select_scustom = scust_stmt.scalars().all()

        #Проверка, что количество записей равно длине переданного списка
        assert len(select_scustom) == len(scustom_list)

    async def test_scustom_user_already_exist(self, db_session):
        """Проверка создания пользователя с уже существующим email."""
        #Подготовка данных
        scustom_repo = ScustomRepository(db_session)
        scust_data = ScustomDataFactory(email = 'Test_Email@gmail.com')
        scust_same_email = ScustomDataFactory(email = 'Test_Email@gmail.com')
        #Добавление и коммит данных в БД
        await scustom_repo.create_scustom_single(scust_data)
        await db_session.commit()

        #Добавление пользователя с уже существующим email
        with pytest.raises(UserAlreadyExistsError) as err:
            await scustom_repo.create_scustom_single(scust_same_email)

        assert err.value

    async def test_get_user_by_email(self, db_session):
        """Проверка выбора пользователя по email."""
        #Подготовка данных
        scustom_repo = ScustomRepository(db_session)
        test_email:str = 'existing@gmail.com'
        nonexistent_email:str = 'nonexistent@gmail.com'

        await scustom_repo.create_scustom_single(ScustomDataFactory(email = test_email))
        await db_session.commit()

        #Выборка существующего пользователя по email
        assert await scustom_repo.get_scustom_by_email(test_email) is not None
        #Выборка несуществующего пользователя по email
        assert await scustom_repo.get_scustom_by_email(nonexistent_email) is None
