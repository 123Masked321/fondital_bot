from sqlalchemy.ext.asyncio import AsyncSession

from database.models import BoilerError
from repositories.boiler_base_repo import BoilerBaseRepository


class BoilerErrorsRepository(BoilerBaseRepository[BoilerError]):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, BoilerError)

    @staticmethod
    def _sort_key(self, code: str) -> tuple[str, int]:
        letters = "".join(ch for ch in code if not ch.isdigit())
        digits = "".join(ch for ch in code if ch.isdigit())
        num = int(digits) if digits else 0
        return letters, num

    async def get_boiler_errors(self, brand_id: int, type_id: int) -> list[BoilerError]:
        errors = await self.list(brand_id=brand_id, type_id=type_id)
        return sorted(errors, key=lambda e: self._sort_key(e.error_code))
