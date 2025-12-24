"""Тесты для сервиса клиентов."""

import pytest

from app.exceptions import UserDoesntExistsError
from tests.factories import ScustomDataFactory


class TestScustomServiceUnit:
    """Unit-тесты для сервиса клиентов."""

    async def test_sign_in_success(self, scustom_service_with_test_user):
        """Тестирование успешной авторизации."""
        scust_auth = await scustom_service_with_test_user.sign_in('TestUser@mail.ru', '88005553535')
        assert scust_auth.auth
    
    async def test_sign_in_wrong_number(self, scustom_service_with_test_user):
        """Тестирование авторизации с неправильным номером телефона."""
        scust_auth = await scustom_service_with_test_user.sign_in('TestUser@mail.ru', '770004442424')
        assert not scust_auth.auth
    
    async def test_sign_in_doesnt_exists_user(self, scustom_service_with_test_user):
        """Тестирование авторизации несуществующего пользователя."""
        with pytest.raises(UserDoesntExistsError):
            await scustom_service_with_test_user.sign_in('DoesntExists@mail.ru', '88005553535')

    async def test_sign_up_success(self, scustom_service_without_data):
        """Тестирование успешной регистрации пользователя."""
        scustom_data = ScustomDataFactory(email = 'TestUser@mail.ru', 
                                        phone_number = '88005553535')
        scustom = await scustom_service_without_data.sign_up(scustom_data.email, scustom_data.phone_number, scustom_data.name)
        assert scustom.auth

    async def test_sign_up_already_exists_user(self, scustom_service_with_test_user):
        """Тестирование регистрации пользователя с существующим email."""
        scustom_data = ScustomDataFactory(email = 'TestUser@mail.ru', 
                                        phone_number = '88005553535')
        scustom = await scustom_service_with_test_user.sign_up(scustom_data.email, scustom_data.phone_number, scustom_data.name)
        assert scustom is None 