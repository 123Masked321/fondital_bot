import os

from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext

from create_bot import bot
from bot.handlers.utils import start_message
from bot.keyboards.main_keyboards import choose_brand_buttons
from bot.keyboards.registration_keyboards import choose_role_button
from bot.middlewares.user_exist_middleware import UserExistMiddleware
from bot.states.registration_states import RegistrationStates
from bot.states.user_states import Boiler

start_router = Router()
start_router.message.middleware(UserExistMiddleware())


@start_router.message(CommandStart())
async def start(message: Message, state: FSMContext, is_registered: bool):
    await state.clear()
    if is_registered:
        brands = await db.get_boiler_brands()
        keyboard = choose_brand_buttons(
            [brand[0] for brand in brands],
            [brand[1] for brand in brands]
        )
        project_root = os.getcwd()
        photo_path = os.path.join(project_root, 'antea.jpg')

        photo = FSInputFile(photo_path)
        await message.answer_photo(photo=photo,
                                   caption=start_message(True),
                                   parse_mode=ParseMode.HTML,
                                   reply_markup=keyboard)
        await state.set_state(Boiler.choose_brand)
    else:
        await message.answer(text=start_message(False),
                             reply_markup=choose_role_button())
        await state.set_state(RegistrationStates.choose_role)
