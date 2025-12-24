"""Модуль, содержащий инструменты для генерации случайных данных для SCARR."""

from faker import Faker

from app.entities.scarr import ScarrData


def generate_scarr(n:int=5)->list[ScarrData]:
    """Генерация списка SCARR для mandt из n позиций."""
    fake = Faker('ru_RU')
    scarr_list:list[ScarrData] = []
    for _ in range(n):
        scarr_list.append(ScarrData(
            carrname = fake.company(),
            carrcode = fake.ean(length=8),
            url = fake.url(),
        ))
    return scarr_list