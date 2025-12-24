"""Фабрики для бронирований."""

import random

import factory
from faker import Faker

from app.entities import SbookData, ScustomData, SflightData

faker = Faker('ru_RU')

class SbookDataFactory(factory.Factory):
    """Фабрика рейсов."""
    class Meta:
        """Описание модели данных."""
        model = SbookData

    _bookid_set = {}
    
    carrid = factory.LazyFunction(lambda: None)
    connid = factory.LazyFunction(lambda: None)
    fldate = factory.LazyFunction(lambda: None)
    bookid = factory.LazyFunction(lambda: None)
    customid = factory.LazyFunction(lambda: None)
    seats = factory.LazyFunction(lambda: None)

    @classmethod
    def build_with_refs(cls, sflight_list: list[SflightData], scustom_list: list[ScustomData]) -> SbookData:
        """Построение через списки зависимых данных."""
        #Множество уникальных дат одинаковых маршрутов
        for sflight in sflight_list:
            if sflight.carrid not in cls._bookid_set:
                cls._bookid_set[sflight.carrid] = {}
            if sflight.connid not in cls._bookid_set[sflight.carrid]:
                cls._bookid_set[sflight.carrid][sflight.connid] = {}
            if sflight.fldate not in cls._bookid_set[sflight.carrid][sflight.connid]:
                cls._bookid_set[sflight.carrid][sflight.connid][sflight.fldate] = 0

        #Выбор случайного перевозчика из списка
        sflight = random.choice(sflight_list)
        #Выбор случайного пользователя
        scustom = random.choice(scustom_list)
        #Получение следующего номера bookid
        new_bookid = cls._bookid_set[sflight.carrid][sflight.connid][sflight.fldate]
        cls._bookid_set[sflight.carrid][sflight.connid][sflight.fldate] += 1

        return cls.build(
            carrid = sflight.carrid,
            connid = sflight.connid,
            fldate = sflight.fldate, 
            bookid = new_bookid,
            customid = scustom.id,
            seats = 1 )
    
    @classmethod
    def build_with_refs_batch(cls, size: int, sflight_list: list[SflightData], scustom_list: list[ScustomData]) -> list[SbookData]:
        """Построение списка через зависимые данные."""
        return [cls.build_with_refs(sflight_list, scustom_list) for _ in range(size)]
    
    @classmethod
    def reset_bookid_set(cls) -> None:
        """Обнуление счетчиков."""
        cls._bookid_set.clear()