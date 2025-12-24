"""Инструменты авторизации пользователя."""
from typing import Self

from prompt_toolkit import PromptSession
from prompt_toolkit.shortcuts.dialogs import radiolist_dialog

from app.database import async_session
from app.entities import ScustomAuth, SflightData
from app.exceptions import (
    NotEnoughSeatsError,
    UserAlreadyExistsError,
    UserDoesntExistsError,
)
from app.services import SairportService, SbookService, ScustomService, SflightService


class Client:
    """Класс клиента."""
    async def __aenter__(self) -> Self:
        """Вход в контекстный менеджер."""
        self._session = async_session()
        self._prompt_session = PromptSession()
        self._sairport_service = SairportService(self._session)
        self._scustom_service = ScustomService(self._session)
        self._sflight_service = SflightService(self._session)
        self._sbook_service = SbookService(self._session)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        """Выход из контекстного менеджера."""
        await self._session.close()


    async def _login(self)->ScustomAuth:
        """Авторизация или регистрация пользователя."""
        print('Авторизация:')
        email:str = await self._prompt_session.prompt_async('Введите Email: ')
        
        try:
            while True:
                phone_number:str = await self._prompt_session.prompt_async('Введите номер телефона: ')
                scust_auth = await self._scustom_service.sign_in(email, phone_number)
                if scust_auth.auth:
                    print('Авторизация пройдена успешно.')
                    break
                else:
                    print('Неверный номер телефона.')
        except UserDoesntExistsError:
            print('Пользователя с таким Email не существует. Зарегистрируйтесь.')
            name = input('ФИО: ')
            try:
                scust_auth = await self._scustom_service.sign_up(email, phone_number, name)
                if scust_auth.auth:
                    print('Регистрация пройдена успешно.')
            except UserAlreadyExistsError:
                scust_auth = None
                print('Ошибка регистрации')

        return scust_auth

    async def _select_cities(self) -> tuple[str, str]:
        """Выбор города отправления и города назначения."""
        #Получение списка городов
        cities = await self._sairport_service.get_uniq_city_list()
        
        result = await radiolist_dialog(
            title='Выбор города',
            text='Выберите город отправления',
            values=list(enumerate(cities)),
        ).run_async()
        if result is None:
            raise KeyboardInterrupt
        city_from = cities[result]
        del cities[result]
        result = await radiolist_dialog(
            title='Выбор города',
            text='Выберите город назначения',
            values=list(enumerate(cities)),
        ).run_async()
        if result is None:
            raise KeyboardInterrupt
        city_to = cities[result]

        return (city_from, city_to)

    async def _select_flight(self, city_from: str, city_to: str)->tuple[dict, int]|None:
        """Выбор рейса между городами."""
        sflight = await self._sflight_service.get_sflights(city_from, city_to)
        if sflight:
            print('Доступные рейсы:')
            for idx, item in enumerate(sflight):
                print(f'Рейс №{idx + 1} на дату {item.fldate} стоимость: {item.price} {item.currency}, количество свободных мест:{item.av_seats}.')
            
            while True:
                selected_flight = int(input('Введите номер выбранного рейса:'))
                seats = int(input('Введите количество мест для бронирования:'))
                if seats > sflight[selected_flight - 1].av_seats:
                    print('В выбранном рейсе недостаточно свободных мест. Выберите другой рейс.')
                else:
                    break

            return sflight[selected_flight - 1], seats
        else:
            return None
        
    async def _book_flight(self, sfl:SflightData, scust:ScustomAuth, seats:int) -> bool:
        """Бронирование выбранного рейса."""
        try:
            return await self._sbook_service.book_flight(sfl, scust, seats)
        except NotEnoughSeatsError:
            print('В рейсе недостаточно свободных мест.')
            return False
    
    async def run(self):
        """Запуск приложения клиента."""
        #Авторизация/Регистрация
        scust_auth = await self._login()
        #Проверка успешности авторизации
        if not scust_auth.auth:
            return
        
        while True:
            #Выбор городов отправления->назначения
            city_from, city_to = await self._select_cities()
            #Выбор рейса с указанием количества мест для бронирования
            select_flight = await self._select_flight(city_from, city_to)
            if not select_flight:
                print('Рейсов для заданных городов не найдено. Выберите другие горда.')
                continue
            selected_flight, seats = select_flight
            break

        #Бронирование выбранного рейса
        if selected_flight and await self._book_flight(selected_flight, scust_auth, seats):
            print('Рейс успешно забронирован.')