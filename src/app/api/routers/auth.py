"""Роуты для аутентификации пользователя."""

from fastapi import APIRouter, HTTPException, Response

from app.auth import auth_config, security
from app.dependencies.services import ScustomServiceDep
from app.exceptions import UserDoesntExistsError
from app.schemas.scustom import ScustomLoginSchema

router = APIRouter(prefix='', tags=['Аутентификация'])

@router.post('/sign_in', summary='Аутентификация пользователя')
async def sign_in(credentials: ScustomLoginSchema, response: Response, service: ScustomServiceDep):
    """Аутентификация пользователя."""
    try:
        scustom_auth = await service.sign_in(credentials.email, credentials.phone_number)
    except UserDoesntExistsError as err:
        raise HTTPException(status_code=401, detail='Incorrect username or phone_number') from err
    
    if scustom_auth.auth:
        token = security.create_access_token(
            uid = str(scustom_auth.id),
            email = scustom_auth.email )
        response.set_cookie(auth_config.JWT_ACCESS_COOKIE_NAME, token)
        return {'access_token': token}
    
    raise HTTPException(status_code=401, detail='Incorrect username or phone_number')