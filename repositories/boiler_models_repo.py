from sqlalchemy.ext.asyncio import AsyncSession
from database.models import BoilerModel
from repositories.boiler_base_repo import BoilerBaseRepository


class BoilerModelsRepository(BoilerBaseRepository[BoilerModel]):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, BoilerModel)

    async def get_boiler_models(self, brand_id: int, type_id: int) -> list[BoilerModel]:
        return await self.list(brand_id=brand_id, type_id=type_id)
