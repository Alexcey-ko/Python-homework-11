"""Фабрики для перевозчиков."""

import factory

from app.schemas import ScarrSchema


class ScarrDataFactory(factory.Factory):
    """Фабрика перевозчиков."""
    class Meta:
        """Описание модели данных."""
        model = ScarrSchema

    carrname = factory.Faker('company', locale = 'ru_RU')
    carrcode = factory.Faker('ean', length = 8, locale = 'ru_RU')
    url = factory.Faker('url', locale = 'ru_RU')