"""SQL запросы для таблицы Sbook."""

from datetime import date

from sqlalchemy import and_, func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from app.cache import Cache
from app.exceptions import NotEnoughSeatsError, SbookDoesntExistsError
from app.models import Sairport, Sbook, Scarr, Sflight, Spfli
from app.repositories.base import Repository
from app.repositories.sflight import SflightRepository
from app.schemas import SbookSchema
from app.schemas.sbook import SbookResponseSchema


class SbookRepository(Repository):
    """SQL запросы для таблицы Sbook."""
    def __init__(self, session: AsyncSession|None, cache: Cache | None = None) -> None:
        """Инициализация объекта."""
        super().__init__(session)
        self.sflight_repo = SflightRepository(self.session, cache)

    async def get_sbooks(self) -> list[SbookResponseSchema]:
        """Получение всех бронирований."""
        sairp_from = aliased(Sairport)
        sairp_to = aliased(Sairport)

        sbooks_query = (
            select(
                Sbook.sbookid,
                Scarr.carrname,
                sairp_from.city.label('cityfrom'),
                Spfli.airpfrom,
                sairp_to.city.label('cityto'),
                Spfli.airpto,
                Spfli.fltime,
                Sflight.price,
                Sflight.currency )
            .join(Sflight, 
                and_(Sflight.carrid == Sbook.carrid, 
                    Sflight.connid == Sbook.connid,
                    Sflight.fldate == Sbook.fldate ))
            .join(Scarr, Scarr.carrid == Sbook.carrid)
            .join(Spfli, 
                and_(Spfli.carrid == Sbook.carrid,
                    Spfli.connid == Sbook.connid))
            .join(sairp_from, sairp_from.id == Spfli.airpfrom)
            .join(sairp_to, sairp_to.id == Spfli.airpto) 
        )
        sbooks_stmt = await self.session.execute(sbooks_query)
        return sbooks_stmt.mappings().all()

    async def get_sbook_by_id(self, sbookid) -> SbookResponseSchema|None:
        """Получение бронирования по ID."""
        sairp_from = aliased(Sairport)
        sairp_to = aliased(Sairport)

        sbooks_query = (
            select(
                Sbook.sbookid,
                Scarr.carrname,
                sairp_from.city.label('cityfrom'),
                Spfli.airpfrom,
                sairp_to.city.label('cityto'),
                Spfli.airpto,
                Spfli.fltime,
                Sflight.price,
                Sflight.currency )
            .join(Sflight, 
                and_(Sflight.carrid == Sbook.carrid, 
                    Sflight.connid == Sbook.connid,
                    Sflight.fldate == Sbook.fldate ))
            .join(Scarr, Scarr.carrid == Sbook.carrid)
            .join(Spfli, 
                and_(Spfli.carrid == Sbook.carrid,
                    Spfli.connid == Sbook.connid))
            .join(sairp_from, sairp_from.id == Spfli.airpfrom)
            .join(sairp_to, sairp_to.id == Spfli.airpto) 
        ).where(Sbook.sbookid == sbookid)
        sbooks_stmt = await self.session.execute(sbooks_query)
        return sbooks_stmt.mappings().one_or_none()

    async def get_sbooks_filtered(self, carrid:int|None = None, connid:int|None = None, fldate: date|None = None) -> list[SbookResponseSchema]:
        """Получение всех бронирований."""
        sairp_from = aliased(Sairport)
        sairp_to = aliased(Sairport)

        #Фильтры
        filters = []
        if carrid is not None:
            filters.append(Sbook.carrid == carrid)
        if connid is not None:
            filters.append(Sbook.connid == connid)
        if fldate is not None:
            filters.append(Sbook.fldate == fldate)

        #Основной запрос
        sbooks_query = (
            select(
                Sbook.sbookid,
                Scarr.carrname,
                sairp_from.city.label('cityfrom'),
                Spfli.airpfrom,
                sairp_to.city.label('cityto'),
                Spfli.airpto,
                Spfli.fltime,
                Sflight.price,
                Sflight.currency )
            .join(Sflight, 
                and_(Sflight.carrid == Sbook.carrid, 
                    Sflight.connid == Sbook.connid,
                    Sflight.fldate == Sbook.fldate ))
            .join(Scarr, Scarr.carrid == Sbook.carrid)
            .join(Spfli, 
                and_(Spfli.carrid == Sbook.carrid,
                    Spfli.connid == Sbook.connid))
            .join(sairp_from, sairp_from.id == Spfli.airpfrom)
            .join(sairp_to, sairp_to.id == Spfli.airpto) 
        ).where(and_(*filters))

        sbooks_stmt = await self.session.execute(sbooks_query)
        #Применение фильтров
        
        return sbooks_stmt.mappings().all()

    async def book_flight(self, carrid:int, connid:int, fldate: date, scustom_id:int, seats:int) -> SbookSchema:
        """Бронирование мест."""
        #Проверка свободных мест
        if seats > await self.sflight_repo.get_av_seats(carrid, connid, fldate):
            raise NotEnoughSeatsError()

        #Выборка Sflight для изменения занятых мест
        sflight_query = select(Sflight).where(
            Sflight.carrid == carrid,
            Sflight.connid == connid,
            Sflight.fldate == fldate)
        sflight_stmt = await self.session.execute(sflight_query)
        sflight:Sflight|None = sflight_stmt.scalar_one_or_none()
        
        #Получение максимального bookid для данного рейса
        max_bookid_query = select(func.max(Sbook.bookid)).where(
            Sbook.carrid == sflight.carrid, 
            Sbook.connid == sflight.connid,
            Sbook.fldate == sflight.fldate)
        max_bookid_stmt = await self.session.execute(max_bookid_query)
        max_bookid = max_bookid_stmt.scalar_one_or_none()
        if not max_bookid:
            max_bookid = 1

        #Изменение количества занятых мест в рейсе
        sflight.seatsocc += seats
        self.session.add(sflight)
        #Подсчет количества свободных мест
        cache_key = f'{sflight.carrid}:{sflight.connid}:{sflight.fldate}'
        av_seats = sflight.seatsmax - sflight.seatsocc
        #Добавление записи бронирования
        new_sbook = Sbook(
            carrid = sflight.carrid,
            connid = sflight.connid,
            fldate = sflight.fldate,
            customid = scustom_id,
            bookid = max_bookid + 1,
            seats = seats
        )
        self.session.add(new_sbook)

        try:
            await self.session.commit()
            if self.cache:
                self.cache.cache_set(cache_key, av_seats, 60 * 60 * 24)
            return SbookSchema(
                    carrid = new_sbook.carrid,
                    connid = new_sbook.connid,
                    fldate = new_sbook.fldate,
                    bookid = new_sbook.bookid,
                    customid = new_sbook.customid,
                    seats = new_sbook.seats )
        except SQLAlchemyError:
            await self.session.rollback()
            return None
        
    async def delete_sbook(self, sbookid: int, scustom_id: int) -> SbookSchema|None:
        """Удаление бронирования."""
        #Выборка бронирования
        sbook_query = select(Sbook).where(
            Sbook.sbookid == sbookid)
        sbook_stmt = await self.session.execute(sbook_query)
        sbook:Sbook|None = sbook_stmt.scalar_one_or_none()
        
        #Бронирования не существует
        if sbook is None:
            raise SbookDoesntExistsError()

        #Проверка владельца бронирования
        if sbook.customid != scustom_id:
            #Пока не нужна
            pass

        #Выборка Sflight для изменения занятых мест
        sflight_query = select(Sflight).where(
            Sflight.carrid == sbook.carrid,
            Sflight.connid == sbook.connid,
            Sflight.fldate == sbook.fldate)
        sflight_stmt = await self.session.execute(sflight_query)
        sflight:Sflight|None = sflight_stmt.scalar_one_or_none()

        #Изменение количества занятых мест в рейсе
        sflight.seatsocc -= sbook.seats
        self.session.add(sflight)
        #Подсчет количества свободных мест
        cache_key = f'{sflight.carrid}:{sflight.connid}:{sflight.fldate}'
        av_seats = sflight.seatsmax - sflight.seatsocc
        #Удаление записи бронирования
        await self.session.delete(sbook)

        try:
            await self.session.commit()
            if self.cache:
                self.cache.cache_set(cache_key, av_seats, 60 * 60 * 24)
            return SbookSchema(
                carrid = sbook.carrid,
                connid = sbook.connid,
                fldate = sbook.fldate,
                bookid = sbook.bookid,
                customid = sbook.customid,
                seats = sbook.seats)
        except SQLAlchemyError:
            await self.session.rollback()
            return None

    def _create_sbook(self, sbook:SbookSchema) -> Sbook:
        """Создание записи в таблице Sbook."""
        new_sbook = Sbook(
            carrid = sbook.carrid,
            connid = sbook.connid,
            fldate = sbook.fldate,
            bookid = sbook.bookid,
            customid = sbook.customid,
            seats = sbook.seats )
        self.session.add(new_sbook)

        return new_sbook

    async def create_sbook_single(self, sbook:SbookSchema) -> SbookSchema:
        """Создание одной записи в таблице Sbook."""
        new_sbook = self._create_sbook(sbook)
        await self.session.flush()

        return SbookSchema(
            carrid = new_sbook.carrid,
            connid = new_sbook.connid,
            fldate = new_sbook.fldate,
            bookid = new_sbook.bookid,
            customid = new_sbook.customid,
            seats = new_sbook.seats )
    
    async def create_sbook_list(self, sbook_list: list[SbookSchema]) -> list[SbookSchema]:
        """Создание одной записи в таблице Sbook."""
        result_list = [self._create_sbook(new_sbook) for new_sbook in sbook_list]
        self.session.add_all(result_list)
        await self.session.flush()

        return [SbookSchema(
                carrid = sbook.carrid,
                connid = sbook.connid,
                fldate = sbook.fldate,
                bookid = sbook.bookid,
                customid = sbook.customid,
                seats = sbook.seats ) for sbook in result_list]
    