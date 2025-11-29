from sqlalchemy.ext.asyncio import AsyncSession
from repositories.base_repo import BaseRepository
from database.models.mediafiles import MediaFile


class MediaFileRepository(BaseRepository[MediaFile]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, MediaFile)

    async def get_by_sha256(self, sha256: str) -> MediaFile | None:
        return await self.get_first(sha256=sha256)

    async def get_by_telegram_unique_id(self, unique_id: str) -> MediaFile | None:
        return await self.get_first(telegram_unique_id=unique_id)
