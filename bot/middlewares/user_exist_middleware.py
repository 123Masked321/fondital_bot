from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

from bot.handlers import start_message
from bot.keyboards.registration_keyboards import choose_role_button
from bot.states.registration_states import RegistrationStates


# Inner-middleware for message
class UserExistMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        is_registered = await db.user_exists(user_id)
        if not is_registered:
            state = data['state']
            await event.answer(text=start_message(False), reply_markup=choose_role_button())
            await state.set_state(RegistrationStates.choose_role)
            return

        data['is_registered'] = is_registered
        return await handler(event, data)
