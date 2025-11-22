from aiogram.filters import BaseFilter
from aiogram.types import Message
from create_bot import db


class IsAdminFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        user_id = message.from_user.id
        role = await db.get_role_user(user_id)
        return role == 'admin'
