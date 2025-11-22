from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.keyboards.admin_keyboards import choose_see_forms_button
from bot.keyboards.main_keyboards import home_button
from bot.states.registration_states import RegistrationStates
from create_bot import bot

registration_router = Router()


@registration_router.callback_query(F.data.startswith("role_"), RegistrationStates.choose_role)
async def get_role(callback: CallbackQuery, state: FSMContext):
    selected_role = callback.data.split("_")[1]
    await state.update_data(role=selected_role)
    if selected_role == "user":
        data = await state.get_data()
        text = f"Регістрация завершена."
        await db.register_user(
            callback.message.chat.username,
            callback.message.chat.id,
            'uk',
            data.get("role"),
            data.get("fullname"),
            data.get("area"),
            data.get("city"),
            data.get("category"),
            data.get("contact"),
            True
        )
        await state.clear()
    else:
        text = "Введіть ПІБ:"
        await state.set_state(RegistrationStates.choose_region)
    await callback.message.answer(text=text)
    await callback.message.delete()


@registration_router.message(F.text, RegistrationStates.choose_region)
async def get_area(message: Message, state: FSMContext):
    await state.update_data(fullname=message.text)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await message.answer(text="Виберіть область:", reply_markup=choose_area_button())
    await state.set_state(RegistrationStates.enter_city)


@registration_router.callback_query(F.data.startswith("area_"), RegistrationStates.enter_city)
async def get_city(callback: CallbackQuery, state: FSMContext):
    selected_area = callback.data.split("_")[1]
    await state.update_data(area=selected_area)
    await callback.message.edit_text("Введіть місто:")
    await state.set_state(RegistrationStates.choose_category)


@registration_router.message(F.text, RegistrationStates.choose_category)
async def get_category(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await message.answer("Виберіть галузь праці:", reply_markup=choose_category_button())
    await state.set_state(RegistrationStates.get_contact)


@registration_router.callback_query(F.data == "change_phone")
@registration_router.callback_query(F.data.startswith("category_"), RegistrationStates.get_contact)
async def get_contact(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Поділіться контактом", reply_markup=get_number_button())
    await callback.message.delete()
    if await state.get_state() == RegistrationStates.get_contact:
        selected_category = callback.data.split("_")[1]
        await state.update_data(category=selected_category)
        await state.set_state(RegistrationStates.registration_user)


@registration_router.message(F.contact, RegistrationStates.registration_user)
async def registration_user(message: Message, state: FSMContext):
    await state.update_data(contact=message.contact.phone_number)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    data = await state.get_data()
    text = (
        f"Заявку залишено. Незабаром з вами зв'яжеться адмін для підтвердження."
        f'Поки що доступні базові функції.'
    )
    if await db.user_exists(message.from_user.id):
        await db.update_user(
            message.chat.id,
            data.get("role"),
            data.get("fullname"),
            data.get("area"),
            data.get("city"),
            data.get("category"),
            data.get("contact"),
            False
        )
    else:
        text_admin = f"✉️Нову заявку на обробку залишено!"
        admins = await db.get_admins()
        for admin in admins:
            await bot.send_message(chat_id=admin["telegram_id"], text=text_admin, parse_mode=ParseMode.HTML,
                                   reply_markup=choose_see_forms_button().as_markup())
        await db.register_user(
            message.chat.username,
            message.chat.id,
            'uk',
            data.get("role"),
            data.get("fullname"),
            data.get("area"),
            data.get("city"),
            data.get("category"),
            data.get("contact"),
            False
        )
    await message.answer(text=text, parse_mode=ParseMode.HTML, reply_markup=home_button().as_markup())


