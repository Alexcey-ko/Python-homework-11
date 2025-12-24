"""Фабрики для перевозчиков."""

import factory

from app.entities.scarr import ScarrData


class ScarrDataFactory(factory.Factory):
    """Фабрика перевозчиков."""
    class Meta:
        """Описание модели данных."""
        model = ScarrData

    carrname = factory.Faker('company', locale = 'ru_RU')
    carrcode = factory.Faker('ean', length = 8, locale = 'ru_RU')
    url = factory.Faker('url', locale = 'ru_RU')