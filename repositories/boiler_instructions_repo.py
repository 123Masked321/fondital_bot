from sqlalchemy.ext.asyncio import AsyncSession
from database.models import BoilerInstructions
from repositories.boiler_base_repo import BoilerBaseRepository


class BoilerInstructionsRepository(BoilerBaseRepository[BoilerInstructions]):
    file_id_attribute: str = 'file_id'

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, BoilerInstructions)

    async def get_boiler_instructions(self, model_id: int) -> list[BoilerInstructions]:
        return await self.list(model_id=model_id)


