"""Зависимости аутентификации."""

from typing import Annotated

from authx import TokenPayload
from fastapi import Depends

from app.auth import security
from app.database import async_session
from app.repositories.scustom import ScustomRepository
from app.schemas.scustom import ScustomSchema


async def get_user_by_uid(payload: Annotated[TokenPayload, Depends(security.access_token_required)]) -> ScustomSchema:
    """Получение пользовтеля из БД."""
    async with async_session() as session:
        scustom_repo = ScustomRepository(session)
        scustom_data = await scustom_repo.get_scustom_by_id(int(payload.sub))
    return scustom_data

AccessTokenUserDep = Annotated[ScustomSchema, Depends(get_user_by_uid)]