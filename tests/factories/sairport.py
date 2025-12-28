"""Фабрики для аэропортов."""

import factory

from app.schemas import SairportSchema


class SairportDataFactory(factory.Factory):
    """Фабрика аэропортов."""
    class Meta:
        """Описание модели данных."""
        model = SairportSchema

    name = factory.Sequence(lambda n: f'Аэропорт {n}')
    city = factory.Sequence(lambda n: f'Город-{n}')
    country = factory.Faker('country', locale='ru_RU')
    timezone = 'UTC+03'