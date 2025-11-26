from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User
from repositories.base_repo import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, User)

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        return await self.get_first(telegram_id=telegram_id)

    async def user_exists(self, telegram_id: int) -> bool:
        return await self.get_by_telegram_id(telegram_id) is not None

    async def get_admin_ids(self) -> list[int]:
        admins = await self.list(role="admin")
        return [admin.telegram_id for admin in admins]

    async def get_users_by_area_and_category(self, area: str, category: str) -> list[User]:
        return await self.list(role='spec', area=area, category=category, is_processed=True)

    async def get_one_user_from_form(self) -> User | None:
        return await self.get_first(role='spec', is_processed=False)

    async def get_count_users(self) -> int:
        return await self.count()

    async def get_count_forms(self) -> int:
        return await self.count(role='spec', is_processed=False)








