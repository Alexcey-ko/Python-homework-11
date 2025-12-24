"""Модуль, содержащий инструменты для генерации случайных данных для SAIRPORT."""

from faker import Faker

from app.entities.sairport import SairportData


def generate_sairport(n:int=5)->list[SairportData]:
    """Генерация списка SAIRPORT для mandt из n позиций."""
    fake = Faker('ru_RU')
    sairport_list:list[SairportData] = []
    for _ in range(n):
        sairport_list.append(
            SairportData(
                name=f'Аэропорт {fake.company()}',
                timezone=fake.timezone(),
                country=fake.country(),
                city=fake.city_name()
            ))
    return sairport_list