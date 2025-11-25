from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from bot.handlers import user
from database.models import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def user_exists(self, telegram_id: int) -> bool:
        q = select(User.id).where(User.telegram_id == telegram_id)
        res = await self.session.execute(q)
        return res.scalar() is not None

    async def get_user_by_telegram_id(self, telegram_id: int) -> User | None:
        q = select(User.id).where(User.telegram_id == telegram_id)
        res = await self.session.execute(q)
        return res.scalars().first()

    async def add_user(self, user: User) -> User:
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def delete_user(self, telegram_id: int) -> None:
        await self.session.delete(user)
        await self.session.commit()

    async def update_user(self, telegram_id: int, data: dict) -> bool:
        values = data.model_dump(exclude_unset=True)
        q = update(User).where(User.telegram_id == telegram_id).values(**values)
        res = await self.session.execute(q)
        await self.session.commit()
        return res.rowco

