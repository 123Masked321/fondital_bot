from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from create_bot import db, bot
from handlers.utils import render_data
from keyboards.main_keyboards import change_info_keyboard, fill_form_keyboard, select_column_keyboard, home_button
from keyboards.registration_keyboards import choose_area_button
from states.user_states import ChangeFullname, ChangeCity

profile_router = Router()


@profile_router.message(Command('profile'))
async def show_profile(message: Message):
    data_user = await db.get_user_data(message.from_user.id)
    text = render_data(data_user)
    markup = fill_form_keyboard() if data_user['role'] == 'user' else change_info_keyboard()
    await message.answer(text=text, parse_mode=ParseMode.HTML, reply_markup=markup)


@profile_router.callback_query(F.data == 'change_info_user')
async def change_info(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    text = 'Виберіть пункт, який бажаєте змінити:'
    await callback.message.edit_text(text=text, parse_mode=ParseMode.HTML, reply_markup=select_column_keyboard())


@profile_router.message(F.contact)
async def update_phone_user(message: Message):
    try:
        await db.update_table('users', 'phone', message.contact.phone_number, message.from_user.id)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id-1)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await message.answer(text='Дані успішно змінені.', reply_markup=home_button().as_markup())
    except Exception as e:
        print(f"Помилка: {e}")


@profile_router.callback_query(F.data == 'change_fullname')
async def change_info(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text="Введіть ПІБ:", reply_markup=home_button().as_markup())
    await state.set_state(ChangeFullname.change_database)


@profile_router.message(F.text, ChangeFullname.change_database)
async def change_info(message: Message):
    try:
        await db.update_table('users', 'fullname', message.text, message.from_user.id)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id-1)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await message.answer(text='Дані успішно змінені.', reply_markup=home_button().as_markup())
    except Exception as e:
        print(f"Помилка: {e}")


@profile_router.callback_query(F.data == 'change_city')
async def change_info(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text="Виберіть область:", reply_markup=choose_area_button())
    await state.set_state(ChangeCity.enter_city)


@profile_router.callback_query(F.data.startswith("area_"), ChangeCity.enter_city)
async def enter_city(callback: CallbackQuery, state: FSMContext):
    selected_area = callback.data.split("_")[1]
    await state.update_data(area=selected_area)
    await callback.message.edit_text("Введіть місто:")
    await state.set_state(ChangeCity.change_database)


@profile_router.message(F.text, ChangeCity.change_database)
async def change_database(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        await db.update_table('users', 'city', message.text, message.from_user.id)
        await db.update_table('users', 'area', data['area'], message.from_user.id)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id-1)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await message.answer(text='Дані успішно змінені.', reply_markup=home_button().as_markup())
    except Exception as e:
        print(f"Помилка: {e}")
