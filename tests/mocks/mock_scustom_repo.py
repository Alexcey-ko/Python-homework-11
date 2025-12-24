"""Моковый репозиторий клиентов."""

from app.entities import ScustomData
from app.exceptions import UserAlreadyExistsError


class MockScustomRepository():
    """Моковый репозиторий клиентов."""

    def __init__(self) -> None:
        """Инициализация репозитория."""
        self._data:list[ScustomData] = []
        self._email_index:dict[str, int] = {}
        self._id_inc: int = 1
        self._unique_email = set()

    async def get_scustom_by_email(self, email:str)->ScustomData|None:
        """Выбор клиента по email."""
        scustom_index = self._email_index.get(email, None)
        return self._data[self._email_index[email]] if scustom_index is not None else None
    
    async def create_scustom_single(self, scustom:ScustomData)->ScustomData:
        """Добавление одного нового клиента."""
        #Проверка, что email ещё не присвоен ни одному пользователю
        if scustom.email in self._unique_email:
            raise UserAlreadyExistsError()
        #Автоматическое проставление ID
        scustom.id = self._id_inc
        self._id_inc += 1
        #Добавление клиента в список
        self._data.append(scustom)
        #Index для поиска по email
        self._email_index[scustom.email] = len(self._data) - 1
        self._unique_email.add(scustom.email)

        return scustom


    async def create_scustom_list(self, scustom_list: list[ScustomData]) -> list[ScustomData]:
        """Создание одной записи в таблице Scustom."""
        unique_email = set(str)
        #Проверка что среди пользователей нету email, который уже присвоен другому пользователю
        #и нету одинаковых email
        for scustom in scustom_list:
            if scustom.email in self._unique_email:
                raise UserAlreadyExistsError()
            if scustom.email in unique_email:
                raise UserAlreadyExistsError()
            unique_email.add(scustom.email)
        #Добавление пользователей по одному
        for scustom in scustom_list:
            scustom = self.create_scustom_single(scustom)