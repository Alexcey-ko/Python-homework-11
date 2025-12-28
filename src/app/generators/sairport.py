"""Модуль, содержащий инструменты для генерации случайных данных для SAIRPORT."""

from faker import Faker

from app.schemas import SairportSchema


def generate_sairport(n:int=5)->list[SairportSchema]:
    """Генерация списка SAIRPORT для mandt из n позиций."""
    fake = Faker('ru_RU')
    sairport_list:list[SairportSchema] = []
    for _ in range(n):
        sairport_list.append(
            SairportSchema(
                name=f'Аэропорт {fake.company()}',
                timezone=fake.timezone(),
                country=fake.country(),
                city=fake.city_name()
            ))
    return sairport_list