from sqlalchemy.ext.asyncio import AsyncSession
from database.models import BoilerType
from repositories.boiler_base_repo import BoilerBaseRepository


class BoilerTypesRepository(BoilerBaseRepository[BoilerType]):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, BoilerType)

    async def get_boiler_types(self) -> list[BoilerType]:
        return await self.list()
