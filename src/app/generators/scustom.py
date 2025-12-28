"""Модуль, содержащий инструменты для генерации случайных данных для SCUSTOM."""

from faker import Faker

from app.schemas import ScustomSchema


def generate_scustom(n:int=5)->list[ScustomSchema]:
    """Генерация списка SCUSTOM для mandt из n позиций."""
    fake = Faker('ru_RU')
    scustom_list:list[ScustomSchema] = []
    for _ in range(n):
        scustom_list.append(ScustomSchema(
            email = fake.email(),
            phone_number = fake.phone_number(),
            name = fake.name(),
        ))
    return scustom_list