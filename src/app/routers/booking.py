"""Роуты для работы с бронированием рейсов."""

from typing import Annotated, Optional

from fastapi import APIRouter, HTTPException, Path

from app.dependencies import AccessTokenUserDep, SbookServiceDep
from app.exceptions import NotEnoughSeatsError, SbookDoesntExistsError
from app.schemas.sbook import BookingSchema, SbookResponseSchema, SbookSchema

router = APIRouter(prefix='', tags=['Бронирование'])

@router.get('/books', 
            summary='Получение списка бронирований', 
            response_model=list[SbookResponseSchema]
)
async def get_books(service: SbookServiceDep)  -> list[SbookResponseSchema]:
    """Получение списка всех бронирований."""
    return await service.get_sbooks()

@router.get('/books/{sbookid}',
            summary='Получение бронирования по ID',
            response_model=Optional[SbookResponseSchema]
)
async def get_book_by_id(
    sbookid: Annotated[int, Path(..., description = 'ID бронирования')],
    service: SbookServiceDep, 
)  -> Optional[SbookResponseSchema]:
    """Получение списка всех бронирований."""
    return await service.get_sbook_by_id(sbookid)

@router.post('/books',
            summary='Бронирование рейса',
            response_model = SbookSchema
)
async def book_sflight(
    booking: BookingSchema,
    service: SbookServiceDep,
    scustom: AccessTokenUserDep,
) -> SbookSchema:
    """Бронирование рейса."""
    try:
        return await service.book_flight(booking.carrid, booking.connid, booking.fldate, scustom.id, booking.seats)
    except NotEnoughSeatsError as err:
        raise HTTPException(status_code=409, detail='Not enough seats available for this flight.') from err

@router.delete('/books/{sbookid}',
            summary='Удаление бронирования по ID',
)
async def delete_sbook(
    sbookid: Annotated[int, Path(..., description = 'ID бронирования')],
    service: SbookServiceDep,
    scustom: AccessTokenUserDep,
):
    """Удаление бронирования."""
    try:
        return await service.delete_sbook(sbookid, scustom.id)
    except SbookDoesntExistsError as err:
        raise HTTPException(status_code=404, detail='Booking not found.') from err