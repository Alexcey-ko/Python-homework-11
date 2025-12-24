"""Модуль, содержащий инструменты для генерации случайных данных в БД."""

import asyncio

import app.generators as gens
import app.repositories as repo
from app.cache import cache
from app.database import async_session


def print_routes(sairport_list, spfli_list, sflight_list):
    """Вывод доступных рейсов по городам."""
    #Для удобства тестирования выводится список доступных рейсов город отправления - город назначения
    sairp_city_map = {airp.id: airp.city for airp in sairport_list}
    spfli_routes = {
        (spfli.carrid, spfli.connid): (sairp_city_map[spfli.airpfrom], sairp_city_map[spfli.airpto]) 
        for spfli in spfli_list }
    sflight_routes = {(spfli_route[0], spfli_route[1]): 0 for _, spfli_route in spfli_routes.items()}
    for sflight in sflight_list:
        route = spfli_routes[(sflight.carrid, sflight.connid)]
        sflight_routes[(route[0], route[1])] += 1

    print('Сгенерированные маршруты:')
    for route, count in sflight_routes.items():
        if count > 0:
            print(f'Из города {route[0]} в город {route[1]} доступно {count} рейсов.')

def print_scustoms(scustom_list):
    """Вывод сгенерированных пользователей."""
    #Для удобства тестирования выводится список пользователей
    print('Сгенерированные пользователи:')
    for scustom in scustom_list:
        print(f'{scustom.email} - {scustom.phone_number} - {scustom.name}')

async def generate_all(airp_n: int = 5, carr_n: int = 5, cust_n: int = 5, spfli_n: int = 5, sflight_n: int = 5, sbook_n: int = 5):
    """Генерация данных для всех таблиц и коммит в БД."""
    async with async_session() as session:
        #Для SCARR, SCUSTOM, SAIRPORT: id генерируется на стороне БД, поэтому мы
        #получаем обновленные списки после добавления и flush в БД

        #Генерация клиентов и добавление в БД
        scustom_repo = repo.ScustomRepository(session)
        scustom_list = await scustom_repo.create_scustom_list(gens.generate_scustom(cust_n))

        #Генерация перевозчиков и добавление в БД
        scarr_repo = repo.ScarrRepository(session)
        scarr_list = await scarr_repo.create_scarr_list(gens.generate_scarr(carr_n))

        #Генерация аэропортов и добавление в БД
        sairport_repo = repo.SairportRepository(session)
        sairport_list = await sairport_repo.create_sairport_list(gens.generate_sairport(airp_n))

        #Генерация маршрутов и добавление в БД
        spfli_repo = repo.SpfliRepository(session)
        spfli_list = await spfli_repo.create_spfli_list(gens.generate_spfli(scarr_list, sairport_list, spfli_n))

        #Генерация рейсов и добавление в БД
        sflight_repo = repo.SflightRepository(session, cache)
        sflight_list = await sflight_repo.create_sflight_list(gens.generate_sflight(spfli_list, sflight_n))

        #Генерация бронирований и добавление в БД
        sbook_repo = repo.SbookRepository(session, cache)
        await sbook_repo.create_sbook_list(gens.generate_sbook(sflight_list, scustom_list, sbook_n))
        
        #Кэширование свободных мест
        for item in sflight_list:
            cache.cache_set(f'{item.carrid}:{item.connid}:{item.fldate}', item.seatsmax - item.seatsocc, 60 * 60 * 24)

        #Коммит таблиц в БД
        await session.commit()

        print('Данные успешно сгененрированы и добавлены в БД.')
        print_scustoms(scustom_list)
        print_routes(sairport_list, spfli_list, sflight_list)

if __name__ == '__main__':
    asyncio.run(generate_all(4, 5, 5, 25, 75, 20))