from typing import TypeVar, Optional, Generic, Type
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.base_repo import BaseRepository

Model = TypeVar('Model')


class BoilerBaseRepository(BaseRepository[Model], Generic[Model]):
    description_attribute: str = "description"
    file_id_attribute: str = 'photo_file_id'

    def __init__(self, session: AsyncSession, model: Type[Model]) -> None:
        super().__init__(session, model)

    async def get_file_id_and_description(self, obj_id: int) -> tuple[Optional[str], Optional[int]]:
        obj = await self.get_by_id(obj_id)
        if obj is None:
            return None, None
        return (
            getattr(obj, self.description_attribute),
            getattr(obj, self.file_id_attribute)
        )
