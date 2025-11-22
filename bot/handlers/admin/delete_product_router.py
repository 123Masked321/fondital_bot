from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from create_bot import db, s3
from bot.handlers.admin.admin_router import footer
from bot.keyboards.admin_keyboards import *

delete_product_router = Router()


@delete_product_router.callback_query(F.data == "delete")
async def init_delete(callback: CallbackQuery, state: FSMContext):
    await state.update_data(action=callback.data)
    await callback.message.edit_text(
        text="Виберіть категорію:",
        reply_markup=choose_edit_data_button()
    )
    await state.set_state(DeleteProductStates.processing_data)


@delete_product_router.callback_query(F.data.startswith("data_"), DeleteProductStates.processing_data)
async def choose_delete_item(callback: CallbackQuery, state: FSMContext):
    selected_item = callback.data.split("_")[1]
    await state.update_data(item=selected_item)
    if selected_item == "type":
        types = await db.get_boiler_types()
        markup = choose_type_button(
            [t[0] for t in types],
            [t[1] for t in types]
        )
        text = "Виберіть тип обладнання:"
        await state.set_state(DeleteProductStates.processing_deleting)
    else:
        brands = await db.get_boiler_brands()
        if selected_item == "brand":
            await state.set_state(DeleteProductStates.processing_deleting)
        else:
            await state.set_state(DeleteProductStates.processing_brand)
        text = "Виберіть бренд:"
        markup = choose_brand_button(
            [b[0] for b in brands],
            [b[1] for b in brands]
        )
    await callback.message.edit_text(text=text, reply_markup=markup)


@delete_product_router.callback_query(F.data.startswith("brand_"), DeleteProductStates.processing_brand)
async def choose_area(callback: CallbackQuery, state: FSMContext):
    brand_id = callback.data.split("_")[1]
    await state.update_data(brand=brand_id)
    await state.update_data(brand_name=callback.data.split("_")[2])
    data = await state.get_data()
    if data.get('item') == 'error':
        errors = await db.get_errors(int(brand_id))
        markup = choose_error_buttons(
            [e[0] for e in errors],
            [e[1] for e in errors]
        )
        text = "Виберіть  помилку:"
        await state.set_state(DeleteProductStates.processing_deleting)
    else:
        types = await db.get_boiler_types()
        markup = choose_type_button(
            [t[0] for t in types],
            [t[1] for t in types]
        )
        text = "Виберіть тип обладнання:"
        await state.set_state(DeleteProductStates.processing_type)
    await callback.message.edit_text(text=text, reply_markup=markup)


@delete_product_router.callback_query(F.data.startswith("type_"), DeleteProductStates.processing_type)
async def choose_model(callback: CallbackQuery, state: FSMContext):
    category = int(callback.data.split("_")[1])
    await state.update_data(category=category)
    await state.update_data(category_name=callback.data.split("_")[2])
    data = await state.get_data()
    text = 'Виберіть котел:'
    models = await db.get_models(
        int((await state.get_data())["brand"]),
        category
    )
    markup = choose_model_buttons(
        [m[0] for m in models],
        [m[1] for m in models]
    )
    if data.get('item') == 'instruction':
        await state.set_state(DeleteProductStates.processing_instruction)
    else:
        await state.set_state(DeleteProductStates.processing_deleting)
    await callback.message.edit_text(text=text, reply_markup=markup)


@delete_product_router.callback_query(F.data.startswith("model_"), DeleteProductStates.processing_instruction)
async def choose_instruction(callback: CallbackQuery, state: FSMContext):
    model = callback.data.split("_")[1]
    await state.update_data(model=model)
    await state.update_data(model_name=callback.data.split("_")[2])
    text = "Виберіть інструкцію:"
    instructions = await db.get_instructions(
        int((await state.get_data())["model"]),
        'uk'
    )
    markup = choose_instructions_buttons(
        [i[0] for i in instructions],
        [i[1] for i in instructions]
    )
    await state.set_state(DeleteProductStates.processing_deleting)
    await callback.message.edit_text(text=text, reply_markup=markup)


@delete_product_router.callback_query(F.data == "confirm_edit_product", DeleteProductStates.processing_confirm)
async def confirm_delete(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    title = int(data.get('delete'))
    text = 'Запис видалено\n'
    if data.get("item") == "brand":
        path = await db.get_path_photo_brand(title)
        await db.delete_boiler_brand(title)
    elif data.get("item") == "type":
        path = await db.get_path_photo_type(title)
        await db.delete_boiler_type(title)
    elif data.get("item") == "error":
        path = await db.get_path_photo_error(title)
        await db.delete_boiler_error(title)
    elif data.get("item") == "model":
        path = await db.get_path_photo_model(title)
        await db.delete_boiler_model(title)
    else:
        path = (await db.get_instruction(title)).get('doc_path')
        await db.delete_boiler_instruction(title)
    if path:
        count = await db.count_file(path)
        if count == 0:
            await s3.delete_file(path)
    text += footer()
    await callback.message.edit_text(text=text, reply_markup=choose_action_button())
    await state.clear()