"""SQL запросы для таблицы Scarr."""

from app.models import Scarr
from app.repositories.base import Repository
from app.schemas import ScarrSchema


class ScarrRepository(Repository):
    """SQL запросы для таблицы Scarr."""

    def _create_scarr(self, scarr: ScarrSchema) -> Scarr:
        """Создание записи в таблице Scarr."""
        new_scarr = Scarr(
            carrid = scarr.carrid,
            carrname = scarr.carrname,
            carrcode = scarr.carrcode,
            url = scarr.url,
        )
        self.session.add(new_scarr)

        return new_scarr
    
    async def create_scarr_single(self, scarr: ScarrSchema) -> ScarrSchema:
        """Создание одной записи в таблице Scarr."""
        new_scarr = self._create_scarr(scarr)
        await self.session.flush()

        return ScarrSchema(
                carrid = new_scarr.carrid,
                carrname = new_scarr.carrname,
                carrcode = new_scarr.carrcode,
                url = new_scarr.url )

    async def create_scarr_list(self, scarr_list: list[ScarrSchema]) -> list[ScarrSchema]:
        """Создание одной записи в таблице Scarr."""
        result_list = [self._create_scarr(new_scarr) for new_scarr in scarr_list]
        await self.session.flush()
        
        return [ScarrSchema(
                carrid = scarr.carrid,
                carrname = scarr.carrname,
                carrcode = scarr.carrcode,
                url = scarr.url
            ) for scarr in result_list]      