"""Зависимости сервисов."""

from typing import Annotated

from fastapi import Depends

from app.dependencies.db import AsyncSessionDep
from app.services.sbook import SbookService
from app.services.scustom import ScustomService


def get_scustom_serivce(session: AsyncSessionDep) -> ScustomService:
    """Зависимость для сервиса клиентов."""
    return ScustomService(session)

def get_sbook_serivce(session: AsyncSessionDep) -> SbookService:
    """Зависимость для сервиса бронирований."""
    return SbookService(session)

SbookServiceDep = Annotated[SbookService, Depends(get_sbook_serivce)]

ScustomServiceDep = Annotated[ScustomService, Depends(get_scustom_serivce)]