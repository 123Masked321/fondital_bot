from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.handlers.utils import start_message, build_prompt, send_prompt, get_document_from_s3, send_navigation_message
from bot.keyboards.main_keyboards import *
from bot.states.registration_states import RegistrationStates

from bot.states.user_states import Boiler
from create_bot import bot

user_router = Router()


# async def choose_language(message: Message):
#     keyboard = choose_lang_button()
#     await message.answer("Оберіть мову:", reply_markup=keyboard)
#
#
# @user_router.message(Command("language"))
# async def language(message: Message):
#     await choose_language(message)


@user_router.callback_query(F.data.startswith("brand_"), Boiler.choose_brand)
async def choose_category(callback: CallbackQuery, state: FSMContext, db: AsyncSession):
    await state.clear()
    selected_brand = int(callback.data.split("_")[1])
    await state.update_data(brand=selected_brand)
    details_brand = await db.get_details_brand(selected_brand)
    text = build_prompt(details_brand.get('description_uk'), 'Виберіть тип обладнання:')
    await send_prompt(callback.message, state, db.get_boiler_types, keyboard_fn=choose_category_buttons,
                      photo_path=details_brand.get('photo_path'), text=text, next_state=Boiler.choose_category)


@user_router.callback_query(F.data.startswith("type_"), Boiler.choose_category)
async def process_category(callback: CallbackQuery, state: FSMContext):
    category = int(callback.data.split("_")[1])
    await state.update_data(category=category)
    data = await state.get_data()
    brand = int(data["brand"])
    details_category = await db.get_details_type(category)
    text = build_prompt(details_category.get('description_uk'), 'Виберіть модель обладнання:')
    await send_prompt(callback.message, state, db.get_models, brand, category, keyboard_fn=choose_model_buttons,
                      photo_path=details_category.get('photo_path'), text=text, next_state=Boiler.choose_model)


@user_router.callback_query(F.data == "error", Boiler.choose_category)
async def process_category(callback: CallbackQuery, state: FSMContext):
    await state.update_data(category=F.data)
    data = await state.get_data()
    brand = int(data["brand"])
    details_brand = await db.get_details_brand(brand)
    text = build_prompt(details_brand.get('description_uk'), 'Виберіть код помилки:')
    await send_prompt(callback.message, state, db.get_errors, brand, keyboard_fn=choose_error_buttons,
                      photo_path=details_brand.get('photo_path'), text=text, next_state=Boiler.choose_error)


@user_router.callback_query(F.data.startswith("error_"), Boiler.choose_error)
async def process_error(callback: CallbackQuery, state: FSMContext):
    error_id = int(callback.data.split("_")[1])
    details_error = await db.get_details_error(error_id)
    caption = f'<b>{details_error["error_code"]}</b>\n{details_error["description_uk"]}'
    if details_error["photo_path"]:
        file = await get_document_from_s3(details_error["photo_path"])
        await callback.message.answer_photo(photo=file, caption=caption, parse_mode=ParseMode.HTML)
    else:
        await callback.message.answer(text=caption)
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    await state.set_state(Boiler.choose_detail_error)
    await send_navigation_message(callback.message)


@user_router.callback_query(F.data.startswith("model_"), Boiler.choose_model)
async def process_model(callback: CallbackQuery, state: FSMContext):
    model = int(callback.data.split("_")[1])
    await state.update_data(model=model)
    details_model = await db.get_details_model(model)
    text = build_prompt(details_model.get('description_uk'), 'Виберіть інструкція:')
    await send_prompt(callback.message, state, db.get_instructions, model, keyboard_fn=choose_instructions_buttons,
                      photo_path=details_model.get('photo_path'), text=text, next_state=Boiler.choose_instruction)


@user_router.callback_query(F.data.startswith("instr_"), Boiler.choose_instruction)
async def process_instruction(callback: CallbackQuery, state: FSMContext):
    instruction = callback.data.split("_")[1]
    doc = await db.get_instruction(int(instruction))

    if doc.get('role') == 'user':
        file = await get_document_from_s3(doc.get('doc_path'))
        await bot.send_document(chat_id=callback.message.chat.id, document=file, caption=doc.get('doc_type'))
        await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    else:
        if await db.get_role_user(callback.from_user.id) == 'user':
            await callback.message.edit_caption(caption="Доступно лише для фахівців.\nВи можете спробувати подати заяву.",
                                             reply_markup=fill_form_keyboard(True))
            await state.set_state(RegistrationStates.choose_role)
            return
        else:
            if await db.check_processed_spec(callback.from_user.id):
                file = await get_document_from_s3(doc.get('doc_path'))
                await bot.send_document(chat_id=callback.message.chat.id, document=file, caption=doc.get('doc_type'))
                await bot.delete_message(callback.message.chat.id, callback.message.message_id)
            else:
                await callback.message.edit_caption(caption="Доступно лише для фахівців.\n"
                                                 "Зачекайте, поки адмін обробить вашу заяву")
    await send_navigation_message(callback.message)
    await state.set_state(Boiler.choose_detail_instruction)


# @user_router.callback_query(F.data.startswith("lang_"))
# async def process_language_selection(callback: CallbackQuery, state: FSMContext):
#     lang_code = callback.data.split("_")[1]
#     if await db.user_exists(callback.from_user.id):
#         await db.update_lang_user(callback.from_user.id, lang_code)
#     else:
#         await db.register_user(callback.from_user.full_name, callback.from_user.id, lang_code)
#     await callback.message.edit_text(f"Спасибо! Язык установлен на {'Українська' if lang_code == 'uk' else 'Русский'}.")
#     await choose_boiler_brand(callback.message, state)


@user_router.callback_query(F.data == "home")
async def main_menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await send_prompt(callback.message, state, db.get_boiler_brands, keyboard_fn=choose_brand_buttons,
                      photo_path='antea.jpg', text=start_message(True), next_state=Boiler.choose_brand)
    await state.set_state(Boiler.choose_brand)


@user_router.callback_query(F.data == "back")
async def go_back(callback: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    data = await state.get_data()

    if current_state == Boiler.choose_category:
        await send_prompt(callback.message, state, db.get_boiler_brands, keyboard_fn=choose_brand_buttons,
                          photo_path=None, text=start_message(True), next_state=Boiler.choose_brand)

    elif current_state in (Boiler.choose_error, Boiler.choose_model):
        details_brand = await db.get_details_brand(int(data.get('brand')))
        text = build_prompt(details_brand.get('description_uk'), 'Виберіть тип обладнання:')
        await send_prompt(callback.message, state, db.get_boiler_types, keyboard_fn=choose_category_buttons,
                          photo_path=details_brand.get('photo_path'), text=text, next_state=Boiler.choose_category)

    elif current_state == Boiler.choose_detail_error:
        brand = int(data.get('brand'))
        details_brand = await db.get_details_brand(brand)
        text = build_prompt(details_brand.get('description_uk'), 'Виберіть код помилки:')
        errors = await db.get_errors(brand)
        markup = choose_error_buttons(
            [i[0] for i in errors],
            [i[1] for i in errors]
        )
        photo = details_brand.get('photo_path')
        await callback.message.answer(text=text, reply_markup=markup)
        await state.set_state(Boiler.choose_error)

    elif current_state == Boiler.choose_instruction:
        details_brand = int(data.get('brand'))
        category = int(data.get('category'))
        details_category = await db.get_details_type(category)
        text = build_prompt(details_category.get('description_uk'), 'Виберіть модель обладнання:')
        await send_prompt(callback.message, state, db.get_models, details_brand, category,
                          keyboard_fn=choose_model_buttons, photo_path=details_category.get('photo_path'),
                          text=text, next_state=Boiler.choose_model)

    elif current_state == Boiler.choose_detail_instruction:
        model = int(data.get('model'))
        details_model = await db.get_details_model(model)
        text = build_prompt(details_model.get('description_uk'), 'Виберіть інструкція:')
        instructions = await db.get_instructions(model)
        markup = choose_instructions_buttons(
            [i[0] for i in instructions],
            [i[1] for i in instructions]
        )
        await callback.message.answer(text=text, reply_markup=markup)
        await state.set_state(Boiler.choose_instruction)

    else:
        await send_prompt(callback.message, state, db.get_boiler_brands, keyboard_fn=choose_brand_buttons,
                          photo_path=None, text=start_message(True), next_state=Boiler.choose_brand)
