from typing import TypeVar, Optional, Generic, Type
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.base_repo import BaseRepository

Model = TypeVar('Model')


class BoilerBaseRepository(BaseRepository[Model], Generic[Model]):
    description_attribute: str = 'description'
    photo_from_s3_url_attribute: str = 'photo_path_from_s3'
    photo_from_telegram_id_attribute: str = 'photo_path_telegram_id'

    def __init__(self, session: AsyncSession, model: Type[Model]) -> None:
        super().__init__(session, model)

    async def get_path_and_description(self, obj_id: int) -> tuple[Optional[str], Optional[str], Optional[str]]:
        obj = await self.get_by_id(obj_id)
        if obj is None:
            return None, None, None
        return (
            getattr(obj, self.photo_from_s3_url_attribute),
            getattr(obj, self.photo_from_telegram_id_attribute),
            getattr(obj, self.description_attribute)
        )
