"""Функции для работы с пользователями."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import UserAlreadyExistsError, UserDoesntExistsError
from app.repositories.scustom import ScustomRepository
from app.schemas import ScustomAuthSchema, ScustomSchema


class ScustomService:
    """Класс-сервис аэропортов."""
    def __init__(self, session: AsyncSession):
        """Инициализация сервиса."""
        self.scust_repo = ScustomRepository(session)

    async def sign_in(self, email:str, phone_number:str) -> ScustomAuthSchema:
        """Авторизация пользователя.

        Args:
            email (str): email пользователя
            phone_number (str): номер телефона пользователя

        Returns:
            ScustomAuthSchema: результат авторизации
        """
        scustom = await self.scust_repo.get_scustom_by_email(email)
        if scustom:
            return ScustomAuthSchema(
                    id = scustom.id,
                    email = scustom.email,
                    auth = phone_number == scustom.phone_number )
        else:
            raise UserDoesntExistsError

    async def sign_up(self, email:str, phone_number:str, name:str) -> ScustomAuthSchema|None:
        """Регистрация пользователя.

        Args:
            email (str): email пользователя
            phone_number (str): номер телефона пользователя
            name (str): ФИО пользователя
        """
        scust_data = ScustomSchema(
                        email = email, 
                        phone_number = phone_number, 
                        name = name )
        try:
            scustom = await self.scust_repo.create_scustom_single(scust_data)
        except UserAlreadyExistsError:
            return None
        
        if scustom:
            return ScustomAuthSchema(
                    id = scustom.id,
                    email = scustom.email,
                    auth = phone_number == scustom.phone_number )