"""Модуль, содержащий инструменты для генерации случайных данных для SCARR."""

from faker import Faker

from app.schemas import ScarrSchema


def generate_scarr(n:int=5)->list[ScarrSchema]:
    """Генерация списка SCARR для mandt из n позиций."""
    fake = Faker('ru_RU')
    scarr_list:list[ScarrSchema] = []
    for _ in range(n):
        scarr_list.append(ScarrSchema(
            carrname = fake.company(),
            carrcode = fake.ean(length=8),
            url = fake.url(),
        ))
    return scarr_list