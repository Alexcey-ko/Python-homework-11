"""Фабрики для клиентов."""

import factory

from app.entities.scustom import ScustomData


class ScustomDataFactory(factory.Factory):
    """Фабрика клиентов."""
    class Meta:
        """Описание модели данных."""
        model = ScustomData

    email = factory.Faker('email', locale = 'ru_RU')
    phone_number = factory.Faker('phone_number', locale = 'ru_RU')
    name = factory.Faker('name', locale = 'ru_RU')