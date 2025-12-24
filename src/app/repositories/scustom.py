"""SQL запросы для таблицы Scustom."""

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.entities import ScustomData
from app.exceptions import UserAlreadyExistsError
from app.models import Scustom
from app.repositories.base import Repository


class ScustomRepository(Repository):
    """SQL запросы для таблицы Scustom."""

    async def get_scustom_by_email(self, email:str)->ScustomData|None:
        """Выбор клиента по email."""
        query = select(Scustom).where(Scustom.email == email)
        stmt = await self.session.execute(query)
        scust = stmt.scalar_one_or_none()

        if scust:
            return ScustomData(
                    id = scust.id,
                    email = scust.email,
                    phone_number = scust.phone_number,
                    name = scust.name )

    def _create_scustom(self, scustom:ScustomData)->Scustom:
        """Добавление нового клиента."""
        new_scustom = Scustom(
            email = scustom.email, 
            phone_number = scustom.phone_number, 
            name = scustom.name )
        self.session.add(new_scustom)

        return new_scustom
    
    async def create_scustom_single(self, scustom:ScustomData)->ScustomData:
        """Добавление одного нового клиента."""
        new_scustom = self._create_scustom(scustom)
        try:
            await self.session.commit()
        except IntegrityError as err:
            raise UserAlreadyExistsError from err

        return ScustomData(
                id = new_scustom.id,
                email = new_scustom.email,
                phone_number = new_scustom.phone_number,
                name = new_scustom.name )

    async def create_scustom_list(self, scustom_list: list[ScustomData]) -> list[ScustomData]:
        """Создание одной записи в таблице Scustom."""
        result_list = [self._create_scustom(new_scustom) for new_scustom in scustom_list]
        try:
            await self.session.flush()
        except IntegrityError as err:
            raise UserAlreadyExistsError from err
        
        return [ScustomData(
                id = scust.id,
                email = scust.email,
                phone_number = scust.phone_number,
                name = scust.name
            ) for scust in result_list]