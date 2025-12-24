"""Модуль, содержащий инструменты для генерации случайных данных для SFLIGHT."""

import random
import string
from datetime import date, timedelta
from decimal import Decimal

from faker import Faker

from app.entities.sflight import SflightData
from app.entities.spfli import SpfliData


def generate_planetype():
    """Генерация типа самолета."""
    letter = random.choice(string.ascii_uppercase)
    number = random.randint(100, 999)
    return f'{letter}{number}'

def generate_sflight(spfli:list[SpfliData], n:int=5)->list[SflightData]:
    """Генерация списка SFLIGHT для mandt из n позиций."""
    faker = Faker()
    sflight_list = []
    today = date.today()

    fldate_set = {}
    #Для соблюдения уникальности ключа, заведем множества дат в разрезе carid+connid
    for item in spfli:
        if item.carrid not in fldate_set:
            fldate_set[item.carrid] = {}
        fldate_set[item.carrid][item.connid] = set()

    for _ in range(n):
        spfl = random.choice(spfli)
        smax = random.randint(50, 300)

        while True:
            new_fldate = faker.date_between(today, today + timedelta(days=160))
            if new_fldate not in fldate_set[spfl.carrid][spfl.connid]:
                fldate_set[spfl.carrid][spfl.connid].add(new_fldate)
                break

        sflight_list.append(SflightData(
            carrid = spfl.carrid,
            connid = spfl.connid,
            fldate = new_fldate,
            price = Decimal(f'{random.uniform(50, 1500):.2f}'),
            currency = faker.currency_code(),
            planetype = generate_planetype(),
            seatsmax = smax,
            seatsocc = 0,
            av_seats = smax ))
    return sflight_list