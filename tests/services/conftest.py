"""Фикстуры для тестирования сервисов."""

import pytest

from app.services import ScustomService
from tests.factories import ScustomDataFactory
from tests.mocks import MockScustomRepository


@pytest.fixture
def scustom_service_without_data():
    """Сервис клиентов с моковым репозиторием."""
    scust_service = ScustomService(None)
    scust_service.scust_repo = MockScustomRepository()
    return scust_service

@pytest.fixture
async def scustom_service_with_test_user():
    """Сервис клиентов с моковым репозиторием."""
    scust_service = ScustomService(None)
    mock_scust_repo = MockScustomRepository()
    await mock_scust_repo.create_scustom_single(ScustomDataFactory(email = 'TestUser@mail.ru', 
                                                                phone_number = '88005553535'))
    scust_service.scust_repo = mock_scust_repo 
    print(scust_service.scust_repo._data)
    return scust_service