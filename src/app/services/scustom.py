"""Функции для работы с пользователями."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.entities import ScustomAuth, ScustomData
from app.exceptions import UserAlreadyExistsError, UserDoesntExistsError
from app.repositories.scustom import ScustomRepository


class ScustomService:
    """Класс-сервис аэропортов."""
    def __init__(self, session: AsyncSession|None):
        """Инициализация сервиса."""
        self.session = session
        self.scust_repo = ScustomRepository(self.session)

    async def sign_in(self, email:str, phone_number:str) -> ScustomAuth:
        """Авторизация пользователя.

        Args:
            email (str): email пользователя
            phone_number (str): номер телефона пользователя

        Returns:
            bool: результат авторизации
        """
        scustom = await self.scust_repo.get_scustom_by_email(email)
        if scustom:
            return ScustomAuth(
                    id = scustom.id,
                    email = scustom.email,
                    auth = phone_number == scustom.phone_number )
        else:
            raise UserDoesntExistsError

    async def sign_up(self, email:str, phone_number:str, name:str) -> ScustomAuth|None:
        """Регистрация пользователя.

        Args:
            email (str): email пользователя
            phone_number (str): номер телефона пользователя
            name (str): ФИО пользователя
        """
        scust_data = ScustomData(
                        email = email, 
                        phone_number = phone_number, 
                        name = name )
        try:
            scustom = await self.scust_repo.create_scustom_single(scust_data)
        except UserAlreadyExistsError:
            return None
        
        if scustom:
            return ScustomAuth(
                    id = scustom.id,
                    email = scustom.email,
                    auth = phone_number == scustom.phone_number )
