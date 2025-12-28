"""SQL запросы для таблицы Spfli."""

from app.models import Spfli
from app.repositories.base import Repository
from app.schemas import SpfliSchema


class SpfliRepository(Repository):
    """SQL запросы для таблицы Spfli."""

    def _create_spfli(self, spfli: SpfliSchema) -> Spfli:
        """Создание записи в таблице Spfli."""
        new_spfli = Spfli(
            carrid = spfli.carrid,
            connid = spfli.connid,
            airpfrom = spfli.airpfrom,
            airpto = spfli.airpto,
            fltime = spfli.fltime )

        return new_spfli
    
    async def create_spfli_single(self, spfli: SpfliSchema) -> SpfliSchema:
        """Создание одной записи в таблице Spfli."""
        new_spfli = self._create_spfli(spfli)
        self.session.add(new_spfli)
        await self.session.flush()

        return SpfliSchema(
            carrid = new_spfli.carrid,
            connid = new_spfli.connid,
            airpfrom = new_spfli.airpfrom,
            airpto = new_spfli.airpto,
            fltime = new_spfli.fltime )

    async def create_spfli_list(self, spfli_list: list[SpfliSchema]) -> list[SpfliSchema]:
        """Создание одной записи в таблице Spfli."""
        result_list = [self._create_spfli(new_spfli) for new_spfli in spfli_list]
        self.session.add_all(result_list)
        await self.session.flush()

        return [SpfliSchema(
                carrid = spfli.carrid,
                connid = spfli.connid,
                airpfrom = spfli.airpfrom,
                airpto = spfli.airpto,
                fltime = spfli.fltime ) for spfli in result_list]