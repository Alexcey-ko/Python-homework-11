"""Роуты для работы с бронированием рейсов."""

from datetime import date
from typing import Annotated

from fastapi import APIRouter, Path

from app.dependencies import AccessTokenUserDep, SbookServiceDep
from app.schemas.sbook import SbookResponseSchema, SbookSchema

router = APIRouter(prefix='', tags=['Бронирование'])

@router.get('/books', 
            summary='Получение списка бронирований', 
            response_model=list[SbookResponseSchema]
)
async def get_books(service: SbookServiceDep)  -> list[SbookResponseSchema]:
    """Получение списка всех бронирований."""
    return await service.get_sbooks()

@router.get('/books/{carrid}',
            summary='Получение списка бронирований для конкретного перевозчика',
            response_model=list[SbookResponseSchema]
)
async def get_books_carrid(
    carrid: Annotated[int, Path(..., description = 'ID перевозчика')],
    service: SbookServiceDep, 
)  -> list[SbookResponseSchema]:
    """Получение списка всех бронирований."""
    return await service.get_sbooks_filtered(carrid = carrid)

@router.get('/books/{carrid}/{connid}',
            summary='Получение списка бронирований для конкретного маршрута',
            response_model=list[SbookResponseSchema]
)
async def get_books_spfli(
    carrid: Annotated[int, Path(..., description = 'ID перевозчика')],
    connid: Annotated[int, Path(..., description = 'ID маршрута')],
    service: SbookServiceDep, 
)  -> list[SbookResponseSchema]:
    """Получение списка всех бронирований."""
    return await service.get_sbooks_filtered(carrid = carrid, connid = connid)

@router.get('/books/{carrid}/{connid}/{fldate}',
            summary='Получение списка бронирований для конкретного рейса',
            response_model=list[SbookResponseSchema]
)
async def get_books_sflight(
    carrid: Annotated[int, Path(..., description = 'ID перевозчика')],
    connid: Annotated[int, Path(..., description = 'ID маршрута')],
    fldate: Annotated[date, Path(..., description = 'Дата рейса')],
    service: SbookServiceDep, 
)  -> list[SbookResponseSchema]:
    """Получение списка всех бронирований."""
    return await service.get_sbooks_filtered(carrid = carrid, connid = connid, fldate = fldate)

@router.post('/books/{carrid}/{connid}/{fldate}',
            summary='Бронирование рейса',
            response_model = SbookSchema
)
async def book_sflight(
    carrid: Annotated[int, Path(..., description = 'ID перевозчика')],
    connid: Annotated[int, Path(..., description = 'ID маршрута')],
    fldate: Annotated[date, Path(..., description = 'Дата рейса')],
    service: SbookServiceDep,
    scustom: AccessTokenUserDep,
):
    """Бронирование рейса."""
    return await service.book_flight(carrid, connid, fldate, scustom.id, 1)

@router.delete('/books/{carrid}/{connid}/{fldate}/{bookid}',
            summary='Удаление бронирования',
)
async def delete_sbook(
    carrid: Annotated[int, Path(..., description = 'ID перевозчика')],
    connid: Annotated[int, Path(..., description = 'ID маршрута')],
    fldate: Annotated[date, Path(..., description = 'Дата рейса')],
    bookid: Annotated[int, Path(..., description = 'ID бронирования')],
    service: SbookServiceDep,
    scustom: AccessTokenUserDep,
):
    """Удаление бронирования."""
    return await service.delete_sbook(carrid, connid, fldate, bookid, scustom.id)