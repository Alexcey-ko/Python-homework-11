"""Модуль с тестами для репозитория рейсов."""

import pytest
from sqlalchemy import select

from app.exceptions import NotEnoughSeatsError
from app.models import Sbook, Sflight
from app.repositories import SbookRepository
from tests.factories import SbookDataFactory


@pytest.fixture(autouse = True)
async def clean_sbook_counters():
    """Подготовка зависимых данных для Sbook."""
    SbookDataFactory.reset_bookid_set()

@pytest.mark.asyncio(loop_scope='session')
class TestSbookRepository:
    """Группа тестов репозитория клиентов."""

    async def test_sbook_create_single(self, db_session, sflight_data_list, scustom_data_list):
        """Проверка работы контейнера."""
        #Подготовка данных
        sbook_repo = SbookRepository(db_session)
        sbook_data = SbookDataFactory.build_with_refs(sflight_data_list, scustom_data_list)
        #Добавление и коммит данных в БД
        sbook_data_flush = await sbook_repo.create_sbook_single(sbook_data)
        await db_session.commit()

        #Выборка добавленной записи по ID
        sbook_query = select(Sbook).filter_by(
            carrid = sbook_data_flush.carrid, 
            connid = sbook_data_flush.connid, 
            fldate = sbook_data_flush.fldate,
            bookid = sbook_data_flush.bookid )
        sbook_stmt = await db_session.execute(sbook_query)
        select_sbook = sbook_stmt.scalar_one_or_none()

        #Проверка, что маршрут был найден в БД
        assert select_sbook

    async def test_sbook_create_list(self, db_session, sflight_data_list, scustom_data_list):
        """Проверка работы контейнера."""
        #Подготовка данных
        sbook_repo = SbookRepository(db_session)
        sbook_list = SbookDataFactory.build_with_refs_batch(3, sflight_data_list, scustom_data_list)

        #Добавление и коммит данных в БД
        await sbook_repo.create_sbook_list(sbook_list)
        await db_session.commit()

        #Выборка всех бронирований
        sbook_query = select(Sbook)
        sbook_stmt = await db_session.execute(sbook_query)
        select_sbook = sbook_stmt.scalars().all()

        #Проверка, что количество записей равно длине переданного списка
        assert len(select_sbook) == len(sbook_list)

    async def test_book_flight_success(self, db_session, sflights_with_av_seats, scustom_data):
        """Проверка бронирования рейсов."""
        sbook_repo = SbookRepository(db_session)

        #В рейсах все места свободны. Проверяется создание брони SBOOK и изменение количества мест в SFLIGHT.
        for sflight_data in sflights_with_av_seats:
            seats_to_book = 5
            seatsocc_expected = sflight_data.seatsocc + seats_to_book
            #Бронирование рейса
            book_data = await sbook_repo.book_flight(sflight_data, scustom_data, seats_to_book)

            #Проверка существования брони в БД
            sbook_query = select(Sbook).filter_by(
                carrid = book_data.carrid,
                connid = book_data.connid,
                fldate = book_data.fldate,
                bookid = book_data.bookid)
            sbook_stmt = await db_session.execute(sbook_query)
            select_sbook = sbook_stmt.scalar_one_or_none()
            #Проверка доступных мест после бронирования
            sflight_query = select(Sflight).filter_by(
                carrid = sflight_data.carrid,
                connid = sflight_data.connid,
                fldate = sflight_data.fldate )
            sflight_stmt = await db_session.execute(sflight_query)
            select_sflight = sflight_stmt.scalar_one_or_none()

            #Проверка что бронь создалась
            assert select_sbook
            #Проверка что количество мест изменилось корректно
            assert select_sflight.seatsocc == seatsocc_expected

    async def test_not_enough_seats_book(self, db_session, sflights_with_av_seats, scustom_data):
        """Проверка бронирования рейсов с недостаточным количеством мест."""
        sbook_repo = SbookRepository(db_session)

        #В рейсах все места свободны. Проверяется создание брони SBOOK и изменение количества мест в SFLIGHT.
        for sflight_data in sflights_with_av_seats:
            #Количество мест для бронирования больше доступного
            seats_to_book = sflight_data.seatsmax - sflight_data.seatsocc + 10
            #Бронирование рейса
            with pytest.raises(NotEnoughSeatsError):
                await sbook_repo.book_flight(sflight_data, scustom_data, seats_to_book)