"""Модуль, содержащий инструменты для генерации случайных данных для SPFLI."""

import random

from app.entities.sairport import SairportData
from app.entities.scarr import ScarrData
from app.entities.spfli import SpfliData


def generate_spfli(scarrs:list[ScarrData], sairport:list[SairportData], n:int=5, connid_sync = None)->list[SpfliData]:
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
        spfli_list.append(SpfliData(
            carrid = carrid,
            connid = new_connid,
            fltime = random.randint(20, 1200),#от 20 минут до 20 часов
            airpfrom = airps[0].id,
            airpto = airps[1].id
        ))
    return spfli_list