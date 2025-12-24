"""Фикстуры для тестирования репозиториев."""

from collections import defaultdict

import pytest

from app.repositories import (
    SairportRepository,
    ScarrRepository,
    ScustomRepository,
    SflightRepository,
    SpfliRepository,
)
from tests.factories import (
    SairportDataFactory,
    ScarrDataFactory,
    ScustomDataFactory,
    SflightDataFactory,
    SpfliDataFactory,
)


@pytest.fixture
async def scustom_data(db_session):
    """Подготовка данных Scustom."""
    scustom_repo = ScustomRepository(db_session)
    scustom_data = await scustom_repo.create_scustom_single(ScustomDataFactory())
    await db_session.commit()
    return scustom_data

@pytest.fixture
async def scustom_data_list(db_session):
    """Подготовка данных Scustom."""
    scustom_repo = ScustomRepository(db_session)
    scustom_list = await scustom_repo.create_scustom_list(ScustomDataFactory.build_batch(3))
    await db_session.commit()
    return scustom_list

@pytest.fixture
async def scarr_data_list(db_session):
    """Подготовка данных Scarr."""
    scarr_repo = ScarrRepository(db_session)
    scarr_list = await scarr_repo.create_scarr_list(ScarrDataFactory.build_batch(3))
    await db_session.commit()
    return scarr_list

@pytest.fixture
async def sairport_data_list(db_session):
    """Подготовка данных Sairport."""
    sairp_repo = SairportRepository(db_session)
    sairp_list = await sairp_repo.create_sairport_list(SairportDataFactory.build_batch(2))
    await db_session.commit()
    return sairp_list

@pytest.fixture
async def spfli_data_list(db_session, scarr_data_list, sairport_data_list):
    """Подготовка данных Spfli."""
    spfli_repo = SpfliRepository(db_session)
    spfli_list = await spfli_repo.create_spfli_list(SpfliDataFactory.build_with_refs_batch(3, scarr_data_list, sairport_data_list))
    await db_session.commit()
    return spfli_list

@pytest.fixture
async def sflight_data_list(db_session, spfli_data_list):
    """Подготовка данных Sflight."""
    sflight_repo = SflightRepository(db_session)
    sflight_list = await sflight_repo.create_sflight_list(SflightDataFactory.build_with_refs_batch(3, spfli_data_list))
    await db_session.commit()
    return sflight_list

@pytest.fixture
async def sflight_routes_with_counts(db_session):
    """Заполняет БД рейсами и возвращает количество рейсов по городам отправления и назначения."""
    scarr_repo = ScarrRepository(db_session)
    sairp_repo = SairportRepository(db_session)
    spfli_repo = SpfliRepository(db_session)
    sflight_repo = SflightRepository(db_session)

    #Списко городов
    city_list = ['Саратов', 'Волгоград', 'Москва']
    #Создаем аэропорты по городам
    sairp_list = [
        SairportDataFactory(country = 'Россия', city = city_list[0]), #sairport.id = 1
        SairportDataFactory(country = 'Россия', city = city_list[1]), #sairport.id = 2
        SairportDataFactory(country = 'Россия', city = city_list[2]), #sairport.id = 3
    ]
    #ID обновляется после flush
    sairp_list = await sairp_repo.create_sairport_list(sairp_list)
    #Создаем перевозчиков
    scarr_list = await scarr_repo.create_scarr_list(ScarrDataFactory.build_batch(2))
    #Создаем маршруты по городам
    spfli_list = [
        SpfliDataFactory(
            carrid = scarr_list[0].carrid,
            airpfrom = sairp_list[0].id, #Саратов
            airpto = sairp_list[1].id,   #Волгоград
        ),
        SpfliDataFactory(
            carrid = scarr_list[0].carrid,
            airpfrom = sairp_list[0].id, #Саратов
            airpto = sairp_list[2].id,   #Москва
        ),
        SpfliDataFactory(
            carrid = scarr_list[1].carrid,
            airpfrom = sairp_list[0].id, #Саратов
            airpto = sairp_list[2].id,   #Москва
        ),
        SpfliDataFactory(
            carrid = scarr_list[0].carrid,
            airpfrom = sairp_list[1].id, #Волгоград
            airpto = sairp_list[2].id,   #Москва
        ),
        SpfliDataFactory(
            carrid = scarr_list[0].carrid,
            airpfrom = sairp_list[1].id, #Волгоград
            airpto = sairp_list[0].id,   #Саратов
        ),
        SpfliDataFactory(
            carrid = scarr_list[0].carrid,
            airpfrom = sairp_list[2].id, #Москва
            airpto = sairp_list[0].id,   #Саратов
        )]
    spfli_list = await spfli_repo.create_spfli_list(spfli_list)
    sflight_list = await sflight_repo.create_sflight_list(SflightDataFactory.build_with_refs_batch(10, spfli_list))
    #Коммит всех изменений
    await db_session.commit()

    #Построение мэппинга аэропорт -> город
    sairp_city = {airp.id: airp.city for airp in sairp_list}
    #Построение мэппинга маршурт -> города отправления и назначения
    spfli_cities_map: dict[int, dict[int, tuple[str, str]]] = defaultdict(dict)
    for spfli in spfli_list:
        spfli_cities_map[spfli.carrid][spfli.connid] = (sairp_city[spfli.airpfrom], sairp_city[spfli.airpto])
    #Инициализация всех комбинаций городов отправления-назначения
    result: dict[str, dict[str, int]] = {
        city_from: {city_to: 0 for city_to in city_list if city_to != city_from}
        for city_from in city_list }
    #Подсчет количества рейсов по городам
    for sflight in sflight_list:
        city_from, city_to = spfli_cities_map[sflight.carrid][sflight.connid]
        result[city_from][city_to] += 1

    #Возврат списка кортежей: (город отправления, город назначения, количество рейсов)
    return [ (city_from, city_to, count) 
            for city_from, city_to_map in result.items()
            for city_to, count in city_to_map.items() ]

@pytest.fixture
async def sflights_with_av_seats(db_session):
    """Заполняет БД рейсами и возвращает количество рейсов по городам отправления и назначения."""
    scarr_repo = ScarrRepository(db_session)
    sairp_repo = SairportRepository(db_session)
    spfli_repo = SpfliRepository(db_session)
    sflight_repo = SflightRepository(db_session)

    #Заполнение таблиц
    sairp_list = await sairp_repo.create_sairport_list(SairportDataFactory.build_batch(3))
    scarr_list = await scarr_repo.create_scarr_list(ScarrDataFactory.build_batch(2))
    spfli_list = await spfli_repo.create_spfli_list(SpfliDataFactory.build_with_refs_batch(5, scarr_list, sairp_list))
    sflight_list = await sflight_repo.create_sflight_list(SflightDataFactory.build_with_refs_batch(10, spfli_list))
    #Коммит всех изменений
    await db_session.commit()

    #Возврат списка рейсов
    return sflight_list