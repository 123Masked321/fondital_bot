from io import BytesIO

from aiogram import Router, F
from aiogram.client.session import aiohttp
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from create_bot import bot, db, s3, TOKEN
from bot.handlers.admin.admin_router import footer
from bot.handlers.utils import render_data
from bot.keyboards.admin_keyboards import *

add_product_router = Router()



@add_product_router.callback_query(F.data == "add")
async def choose_category(callback: CallbackQuery, state: FSMContext):
    await state.update_data(action=callback.data)
    await callback.message.edit_text(
        text="Виберіть категорію:",
        reply_markup=choose_edit_data_button()
    )
    await state.set_state(AddProductStates.processing_data)


@add_product_router.callback_query(F.data.startswith("data_"), AddProductStates.processing_data)
async def choose_brand(callback: CallbackQuery, state: FSMContext):
    selected_item = callback.data.split("_")[1]
    await state.update_data(item=selected_item)
    if selected_item in ("brand", "type"):
        text = 'Введіть назву бренду:' if selected_item == 'brand' else 'Введіть тип обладнання:'
        markup = None
        await state.set_state(AddProductStates.processing_title)
    else:
        brands = await db.get_boiler_brands()
        markup = choose_brand_button(
            [b[0] for b in brands],
            [b[1] for b in brands]
        )
        await state.set_state(AddProductStates.processing_brand)
        text = "Виберіть бренд:"
    await callback.message.edit_text(text, reply_markup=markup)


@add_product_router.callback_query(F.data.startswith("brand_"), AddProductStates.processing_brand)
async def choose_area(callback: CallbackQuery, state: FSMContext):
    brand_id = callback.data.split("_")[1]
    await state.update_data(brand=brand_id)
    await state.update_data(brand_name=callback.data.split("_")[2])
    data = await state.get_data()
    if data.get('item') == 'error':
        text = 'Введіть код помилки:'
        markup = None
        await state.set_state(AddProductStates.processing_title)
    else:
        types = await db.get_boiler_types()
        markup = choose_type_button(
            [t[0] for t in types],
            [t[1] for t in types]
        )
        text = "Виберіть тип обладнання:"
        await state.set_state(AddProductStates.processing_type)
    await callback.message.edit_text(text=text, reply_markup=markup)


@add_product_router.callback_query(F.data.startswith("type_"), AddProductStates.processing_type)
async def choose_model(callback: CallbackQuery, state: FSMContext):
    category = int(callback.data.split("_")[1])
    await state.update_data(category=category)
    await state.update_data(category_name=callback.data.split("_")[2])
    data = await state.get_data()
    if data.get('item') == 'model':
        text = 'Введіть модель обладнання:'
        markup = None
        await state.set_state(AddProductStates.processing_title)
    else:
        text = 'Виберіть котел:'
        models = await db.get_models(
            int((await state.get_data())["brand"]),
            category
        )
        markup = choose_model_buttons(
            [m[0] for m in models],
            [m[1] for m in models]
        )
        await state.set_state(AddProductStates.processing_instruction)
    await callback.message.edit_text(text=text, reply_markup=markup)


@add_product_router.callback_query(F.data.startswith("model_"), AddProductStates.processing_instruction)
async def choose_instruction(callback: CallbackQuery, state: FSMContext):
    model = callback.data.split("_")[1]
    await state.update_data(model=model)
    await state.update_data(model_name=callback.data.split("_")[2])
    await callback.message.edit_text("Введіть назву інструкції:")
    await state.set_state(AddProductStates.processing_document)


@add_product_router.message(F.text, AddProductStates.processing_title)
async def enter_title(message: Message, state: FSMContext):
    await state.update_data(title=message.html_text)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await state.set_state(AddProductStates.processing_document)
    await message.answer("Введіть опис:", reply_markup=choose_skip_button())


@add_product_router.message(F.text, AddProductStates.processing_document)
async def enter_description(message: Message, state: FSMContext):
    if message.text == 'Пропустити':
        await state.update_data(description=None)
    else:
        await state.update_data(description=message.html_text)
    if (await state.get_data()).get('item') == 'instruction':
        text = 'Додайте файл'
        markup = None
    else:
        text = "Додайте фото або Пропустити:"
        markup = choose_skip_button()
    await message.answer(text=text, reply_markup=markup)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await state.set_state(AddProductStates.processing_adding)


@add_product_router.message(F.text == "Пропустити", AddProductStates.processing_adding)
@add_product_router.message(F.content_type.in_({"photo", "document"}), AddProductStates.processing_adding)
async def finalize_add(message: Message, state: FSMContext):
    if message.document and (await state.get_data()).get('item') == 'instruction':
        file = message.document
        file_name = file.file_name
        text = f'Оберіть рівень доступ до файлу:'
        markup = choose_group_persons_buttons()
        await state.set_state(AddProductStates.processing_access)
    else:
        data = await state.get_data()
        if message.photo:
            file = message.photo[-1]
            file_name = f"photo_{file.file_id}.jpg"
        else:
            file = None
            file_name = None
        text = render_data(data)
        markup = confirm_add_product_buttons()
    await state.update_data(file=file, file_name=file_name)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await message.answer(text=text, reply_markup=markup)


@add_product_router.callback_query(F.data, DeleteProductStates.processing_deleting)
@add_product_router.callback_query(F.data.startswith("role_"), AddProductStates.processing_access)
async def processing_role(callback: CallbackQuery, state: FSMContext):
    data = callback.data.split("_")[1]
    if (await state.update_data()).get('action') == "add":
        await state.update_data(role=data)
        await state.set_state(AddProductStates.processing_adding)
    else:
        await state.update_data(delete=data)
        await state.update_data(delete_name=callback.data.split("_")[2])
        await state.set_state(DeleteProductStates.processing_confirm)
    data = await state.get_data()
    text = render_data(data)
    markup = confirm_add_product_buttons()
    await callback.message.edit_text(text=text, reply_markup=markup)


@add_product_router.callback_query(F.data == "confirm_edit_product", AddProductStates.processing_adding)
async def confirm_edit_product(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    file = data.get('file')
    file_name = data.get('file_name')
    if file:
        if await db.count_file(file_name) == 0:
            tg_file = await bot.get_file(file.file_id)
            file_url = f"https://api.telegram.org/file/bot{TOKEN}/{tg_file.file_path}"

            async with aiohttp.ClientSession() as session:
                async with session.get(file_url) as response:
                    if response.status != 200:
                        await callback.message.answer("Не удалось загрузить файл из Telegram.")
                        return

                    file_data = BytesIO(await response.read())

            await s3.upload_fileobj(file_data, file_name)

    try:
        if data.get("item") == "brand":
            await db.create_boiler_brand(data.get("title"), data.get("description"), "1", data.get("file_name"))

        elif data.get("item") == "type":
            await db.create_boiler_type(data.get("title"), data.get("description"), "1", data.get("file_name"))

        elif data.get("item") == "error":
            if int(data.get("brand")) == 1 or int(data.get("brand")) == 2:
                await db.create_boiler_error(int('1'), data.get("title"), data.get("description"), "1",
                                             data.get("file_name"))
                await db.create_boiler_error(int('2'), data.get("title"), data.get("description"), "1",
                                             data.get("file_name"))
            else:
                await db.create_boiler_error(int(data.get("brand")), data.get("title"), data.get("description"), "1",
                                             data.get("file_name"))

        elif data.get("item") == "model":
            await db.create_boiler_model(int(data.get("brand")), int(data.get("category")),
                                         data.get("title"), data.get("description"), "1", data.get("file_name"))

        else:
            await db.create_boiler_instruction(int(data.get("model")), data.get("description"), 'uk',
                                               data.get("file_name"), data.get("role"))
        text = 'Запис доданий.\n'
    except Exception as e:
        text = f'Виникла помилка: {e}\n'
    text += footer()
    await callback.message.edit_text(text=text, reply_markup=choose_action_button())
    await state.clear()