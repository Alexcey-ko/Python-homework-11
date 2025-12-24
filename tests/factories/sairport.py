"""Фабрики для аэропортов."""

import factory

from app.entities.sairport import SairportData


class SairportDataFactory(factory.Factory):
    """Фабрика аэропортов."""
    class Meta:
        """Описание модели данных."""
        model = SairportData

    name = factory.Sequence(lambda n: f'Аэропорт {n}')
    city = factory.Sequence(lambda n: f'Город-{n}')
    country = factory.Faker('country', locale='ru_RU')
    timezone = 'UTC+03'