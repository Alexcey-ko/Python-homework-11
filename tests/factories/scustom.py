"""Фабрики для клиентов."""

import factory
from faker import Faker

from app.schemas import ScustomSchema

fake = Faker('ru_RU')
class ScustomDataFactory(factory.Factory):
    """Фабрика клиентов."""
    class Meta:
        """Описание модели данных."""
        model = ScustomSchema

    email = factory.Faker('email', locale = 'ru_RU')
    phone_number = '+7' + fake.numerify('#' * 10)
    name = factory.Faker('name', locale = 'ru_RU')

print(ScustomDataFactory())