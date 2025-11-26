from sqlalchemy.ext.asyncio import AsyncSession

from database.models import BoilerBrand
from repositories.boiler_base_repo import BoilerBaseRepository


class BoilerBrandsRepository(BoilerBaseRepository[BoilerBrand]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, BoilerBrand)

    async def get_boiler_brands(self) -> list[BoilerBrand]:
        return await self.list()
