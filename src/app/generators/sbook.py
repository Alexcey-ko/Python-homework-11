"""Модуль, содержащий инструменты для генерации случайных данных для SBOOK."""

import random

from app.entities.sbook import SbookData
from app.entities.scustom import ScustomData
from app.entities.sflight import SflightData


def generate_sbook(sflight:list[SflightData], scustom:list[ScustomData], n:int=5)->list[SbookData]:
    """Генерация списка SBOOK для mandt из n позиций."""
    sbook:list[SbookData] = []

    seats_av:dict[int] = {} 
    #Расчет свободных мест на рейсах
    for i, sf in enumerate(sflight):
        seats_av[i] = sf.seatsmax - sf.seatsocc

    for _ in range(n):
        #Случайный рейс со свободными местами
        sfl_av_idx, sfl_av_val = random.choice(list(seats_av.items()))
        #Занимаем места в рейсе SFLIGHT
        seats = random.randint(1, sfl_av_val)
        sflight[sfl_av_idx].seatsocc += seats
        #Вычисляем новое количество свободных мест
        seats_av[sfl_av_idx] -= seats
        #Если мест не осталось, исключаем рейс из выбора
        if seats_av[sfl_av_idx] == 0:
            del seats_av[sfl_av_idx]
        #Формируем бронь
        sbook.append(SbookData(
            carrid = sflight[sfl_av_idx].carrid,
            connid = sflight[sfl_av_idx].connid,
            fldate = sflight[sfl_av_idx].fldate,
            bookid = _,
            customid = random.choice(scustom).id,
            seats = seats
        ))
        #Если не осталось рейсов со свободными местами
        if not seats_av:
            break

    return sbook