"""Модуль, содержащий инструменты для генерации случайных данных для SPFLI."""

import random

from app.schemas import SairportSchema, ScarrSchema, SpfliSchema


def generate_spfli(scarrs:list[ScarrSchema], sairport:list[SairportSchema], n:int=5, connid_sync = None)->list[SpfliSchema]:
    """Генерация списка SPFLI для mandt из n позиций."""
    spfli_list = []
    connid_max = connid_sync or {}
    for _ in range(n):
        scarr = random.choice(scarrs)
        airps = random.sample(sairport, 2)
        #Определяем новый connid для carrid
        carrid = scarr.carrid
        new_connid = connid_max.get(carrid, 0) + 1
        connid_max[carrid] = new_connid
        spfli_list.append(SpfliSchema(
            carrid = carrid,
            connid = new_connid,
            fltime = random.randint(20, 1200),#от 20 минут до 20 часов
            airpfrom = airps[0].id,
            airpto = airps[1].id
        ))
    return spfli_list