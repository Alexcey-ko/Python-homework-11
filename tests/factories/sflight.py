"""Фабрики для рейсов."""

import random
import string
from datetime import date, timedelta
from decimal import Decimal

import factory
from faker import Faker

from app.entities import SflightData, SpfliData

faker = Faker('ru_RU')

def generate_planetype():
    """Генерация типа самолета."""
    letter = random.choice(string.ascii_uppercase)
    number = random.randint(100, 999)
    return f'{letter}{number}'

class SflightDataFactory(factory.Factory):
    """Фабрика рейсов."""
    class Meta:
        """Описание модели данных."""
        model = SflightData

    _fldate_set = {}

    carrid = factory.LazyFunction(lambda: None)
    connid = factory.LazyFunction(lambda: None)
    fldate = factory.LazyFunction(lambda: None)
    price = Decimal(f'{random.uniform(50, 1500):.2f}')
    currency = faker.currency_code()
    planetype = generate_planetype()
    seatsmax = random.randint(50, 300)
    seatsocc = 0
    av_seats = seatsmax
    
    @classmethod
    def build_with_refs(cls, spfli_list: list[SpfliData]) -> SflightData:
        """Построение через списки зависимых данных."""
        #Множество уникальных дат одинаковых маршрутов
        for spfl in spfli_list:
            if spfl.carrid not in cls._fldate_set:
                cls._fldate_set[spfl.carrid] = {}
            if spfl.connid not in cls._fldate_set[spfl.carrid]:
                cls._fldate_set[spfl.carrid][spfl.connid] = set()

        #Выбор случайного перевозчика из списка
        spfli = random.choice(spfli_list)
        #Генерация уникальной даты для выбранного маршрута
        today = date.today()
        while True:
            new_fldate = faker.date_between(today, today + timedelta(days=160))
            if new_fldate not in cls._fldate_set[spfl.carrid][spfl.connid]:
                cls._fldate_set[spfl.carrid][spfl.connid].add(new_fldate)
                break

        return cls.build(
            carrid = spfli.carrid,
            connid = spfli.connid,
            fldate = new_fldate )
    
    @classmethod
    def build_with_refs_batch(cls, size: int, spfli_list: list[SpfliData]) -> list[SflightData]:
        """Построение списка через зависимые данные."""
        return [cls.build_with_refs(spfli_list) for _ in range(size)]
    
    @classmethod
    def reset_fldate_set(cls) -> None:
        """Обнуление счетчиков."""
        cls._fldate_set.clear()