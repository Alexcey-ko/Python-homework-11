"""Фабрики для маршрутов."""

import random
from collections import defaultdict

import factory

from app.entities import SairportData, ScarrData, SpfliData


class SpfliDataFactory(factory.Factory):
    """Фабрика маршрутов."""
    class Meta:
        """Описание модели данных."""
        model = SpfliData

    _connid_counters: dict[int, int] = defaultdict(int)

    carrid = factory.LazyFunction(lambda: None)

    @factory.lazy_attribute
    def connid(self) -> int | None:
        """Генерация connid для перевозчика carrid."""
        if self.carrid is None:
            return None

        SpfliDataFactory._connid_counters[self.carrid] += 1
        return SpfliDataFactory._connid_counters[self.carrid]
    
    airpfrom = factory.LazyFunction(lambda: None)
    airpto = factory.LazyFunction(lambda: None)
    fltime = factory.LazyFunction(lambda: random.randint(20, 1200))

    @classmethod
    def build_with_refs(cls, scarr_list: list[ScarrData], sairport_list: list[SairportData]) -> SpfliData:
        """Построение через списки зависимых данных."""
        #Выбор случайного перевозчика из списка
        scarr = random.choice(scarr_list)
        carrid = scarr.carrid
        #Выбор двух разных аэропортов 
        airpfrom, airpto = random.sample(sairport_list, 2)

        return cls.build(
            carrid = carrid,
            airpfrom = airpfrom.id,
            airpto = airpto.id )
    
    @classmethod
    def build_with_refs_batch(cls, size: int, scarr_list: list[ScarrData], sairp_list: list[SairportData]) -> list[SpfliData]:
        """Построение списка через зависимые данные."""
        return [cls.build_with_refs(scarr_list, sairp_list) for _ in range(size)]

    @classmethod
    def reset_counters(cls) -> None:
        """Обнуление счетчиков."""
        cls._connid_counters.clear()