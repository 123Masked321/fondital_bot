from sqlalchemy.ext.asyncio import AsyncSession
from database.models import BoilerInstructions
from repositories.boiler_base_repo import BoilerBaseRepository


class BoilerInstructionsRepository(BoilerBaseRepository[BoilerInstructions]):
    description_attribute: str = 'description'
    photo_from_s3_url_attribute: str = 'doc_path_from_s3'
    photo_from_telegram_id_attribute: str = 'doc_path_telegram_id'

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, BoilerInstructions)

    async def get_boiler_instructions(self, model_id: int) -> list[BoilerInstructions]:
        return await self.list(model_id=model_id)


