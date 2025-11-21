from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from create_bot import bot, db, s3, TOKEN
from filters.is_admin import IsAdminFilter
from keyboards.admin_keyboards import *
from states.admin_states import *

admin_router = Router()


def footer() -> str:
    return f'Оберіть наступну дію:\n'


@admin_router.message(Command('admin'), IsAdminFilter())
async def admin(message: Message):
    await message.answer(text='Оберіть дію:', reply_markup=choose_action_button())


@admin_router.callback_query(F.data.startswith('action_'))
async def action(callback: CallbackQuery, state: FSMContext):
    selected_action = callback.data.split("action_")[1]
    await state.clear()
    if selected_action == 'count_users':
        admin_text = (f'Кількість юзерів: {await db.get_count_users()}\n' + footer())
        markup = choose_action_button()

    elif selected_action == 'check_spec':
        admin_text = f'Виберіть групу осіб(можна декілька):'
        selected_categories = []
        markup = choose_group_specialists_button(selected_categories)
        await state.set_state(SelectSpecStates.choose_category)

    elif selected_action == 'see_forms':
        spec_form_data = await db.get_spec_form()
        if spec_form_data:
            for spec in spec_form_data:
                admin_text = (
                    f'Інформація про спеціаліста:\n'
                    f'👤 ФІО: {spec.get("fullname")}\n'
                    f'📝 Область: {spec.get("area")}\n'
                    f'📝 Місто: {spec.get("city")}\n'
                    f'📝 Посада: {spec.get("category")}\n'
                    f'📝 Номер телефону: {spec.get("phone")}\n'
                )
                markup = choose_answer_spec_button(spec.get("telegram_id"))
                pass
        else:
            admin_text = ('Заявок немає.\n' + footer())
            markup = choose_action_button()

    elif selected_action == 'edit_data':
        admin_text = 'Виберіть дію:'
        markup = choose_action_edit_button()

    else:
        admin_text = 'Виберіть групу осіб, яка отримає повідомлення(можна декілька):'
        selected_categories = []
        markup = choose_group_specialists_button(selected_categories)
        await state.set_state(SendMessages.processing_category)
    await callback.message.edit_text(text=admin_text, reply_markup=markup, parse_mode=ParseMode.HTML)


@admin_router.callback_query(F.data == "go_next_step", SelectSpecStates.choose_category)
async def choose_area(callback: CallbackQuery, state: FSMContext):
    await state.update_data(areas=[])
    admin_text = "Виберіть область(можна декілька):"
    selected_areas = []
    await callback.message.edit_text(text=admin_text, reply_markup=choose_area_buttons(selected_areas))
    await state.set_state(SelectSpecStates.get_info)


async def get_specialists(areas: list, categories: list) -> list:
    spec_data = []
    for area in areas:
        for category in categories:
            specs = await db.get_info_specs(area, category)
            spec_data.extend(specs)
    return spec_data


@admin_router.callback_query(F.data.startswith("go_next_step"), SelectSpecStates.get_info)
async def choose_area(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    spec_data = await get_specialists(data["areas"], data["categories"])

    admin_text = f"Кількість спеціалістів: {len(spec_data)}\n"
    for spec in spec_data:
        admin_text += (
            f'👤 ФІО: {spec.get("fullname")}\n'
            f'📝 Область: {spec.get("area")}\n'
            f'📝 Місто: {spec.get("city")}\n'
            f'📝 Посада: {spec.get("category")}\n'
            f'📝 Номер телефону: {spec.get("phone")}\n'
            f'〰️〰️〰️〰️〰️〰️〰️〰️〰️\n\n'
        )
    admin_text += footer()
    markup = choose_action_button()
    await callback.message.edit_text(text=admin_text, reply_markup=markup, parse_mode=ParseMode.HTML)
    await state.clear()


@admin_router.callback_query(F.data.startswith("answer_"))
async def answer(callback: CallbackQuery):
    selected_action = callback.data.split("_")[1]
    user_id = int(callback.data.split("_")[2])
    if selected_action == "confirm":
        await db.update_answer_form('spec', True, user_id)
        user_text = 'Адмін підтвердив вашу заяву.'
    else:
        await db.update_answer_form('user', True, user_id)
        user_text = 'Адмін відхилив вашу заяву.'
    user_text += ' Натисніть /start для перехода в головне меню'
    await bot.send_message(user_id, text=user_text)
    count_form = await db.get_count_forms()
    admin_text = 'Заявка оброблена.'
    if count_form:
        admin_text += (
            f'Кількість заявок, що залишилися: {count_form}\n' + footer())
        markup = choose_after_form_button()
    else:
        admin_text += (
            'Заявок більше немає.\n' + footer())
        markup = choose_action_button()

    await callback.message.answer(text=admin_text, reply_markup=markup)


@admin_router.callback_query(F.data.startswith("admincategory"))
async def select_category(callback: CallbackQuery, state: FSMContext):
    category = callback.data.split("_")[1]
    data = await state.get_data()
    selected_categories: list[str] = data.get("categories", [])
    if category in selected_categories:
        selected_categories.remove(category)
    else:
        selected_categories.append(category)
    await state.update_data(categories=selected_categories)
    admin_text = 'Виберіть групу осіб(можна декілька):'
    markup = choose_group_specialists_button(selected_categories)
    await callback.message.edit_text(text=admin_text, reply_markup=markup, parse_mode=ParseMode.HTML)


@admin_router.callback_query(F.data == "go_next_step", SendMessages.processing_category)
async def processing_category(callback: CallbackQuery, state: FSMContext):
    await state.update_data(areas=[])
    await callback.message.edit_text(
        text="Оберіть область (можна декілька):",
        reply_markup=choose_area_buttons([])
    )
    await state.set_state(SendMessages.processing_area)


@admin_router.callback_query(F.data.startswith("adminarea_"))
async def toggle_area(callback: CallbackQuery, state: FSMContext):
    _, area = callback.data.split("_")
    data = await state.get_data()
    selected_areas: list[str] = data.get("areas", [])
    if area in selected_areas:
        selected_areas.remove(area)
    else:
        selected_areas.append(area)
    await state.update_data(areas=selected_areas)
    await callback.message.edit_text(
        text="Оберіть області (можна декілька):",
        reply_markup=choose_area_buttons(selected_areas)
    )


@admin_router.callback_query(F.data == "select_all")
async def select_all_aread(callback: CallbackQuery, state: FSMContext):
    await state.update_data(areas=all_areas)
    await callback.message.edit_text(
        text="Оберіть область (можна декілька):",
        reply_markup=choose_area_buttons(all_areas)
    )


@admin_router.callback_query(F.data == "clear_selection")
async def clear_selection_areas(callback: CallbackQuery, state: FSMContext):
    await state.update_data(areas=[])
    await callback.message.edit_text(
        text="Оберіть область (можна декілька):",
        reply_markup=choose_area_buttons([])
    )


@admin_router.callback_query(F.data == "go_next_step", SendMessages.processing_area)
async def processing_category(callback: CallbackQuery, state: FSMContext):
    text = 'Введіть текст повідомлення:'
    await callback.message.edit_text(text=text)
    await state.set_state(SendMessages.processing_text)


@admin_router.message(F.text, SendMessages.processing_text)
async def processing_description(message: Message, state: FSMContext):
    await state.update_data(title=message.html_text)
    data = await state.get_data()
    text = (f'Перевірте інформацію:\n'
            f'<b>Області</b>: {data["areas"]}\n'
            f'<b>Категорії</b>: {data["categories"]}\n'
            f'<b>Текст повідомлення</b>: {data["title"]}')
    markup = confirm_send_messages_buttons()
    await message.answer(text=text, reply_markup=markup)


@admin_router.callback_query(F.data == "confirm_send_messages")
async def confirm_send_messages(callback: CallbackQuery, state: FSMContext):
    # Получаем все данные из FSM
    data = await state.get_data()
    areas = data.get("areas")
    categories = data.get("categories")
    title = data.get("title")

    # Очищаем состояние
    await state.clear()

    sent_count = 0
    errors: list[str] = []

    try:
        # Берём список специалистов из БД
        specialists = await get_specialists(areas, categories)
        specialist_ids = [specialist["telegram_id"] for specialist in specialists]
        for specialist_id in specialist_ids:
            try:
                # Важно: используем callback.bot, чтобы не держать глобальный bot
                await bot.send_message(
                    chat_id=specialist_id,
                    text=title,
                    parse_mode=ParseMode.HTML
                )
                sent_count += 1
            except Exception as e:
                errors.append(f"ID {specialist_id}: {e}")

        # Формируем итоговый текст
        result_text = f"📤 Повідомлення відправлені {sent_count} користувачам.\n"
        if errors:
            result_text += "\n\n❗️Не вдалося надіслати повідомлення для:\n" + "\n".join(errors)

    except Exception as e:
        result_text = f"❌ Виникла помилка при отриманні спеціалістів: {e}"

    result_text += footer()

    await callback.message.edit_text(text=result_text, parse_mode=ParseMode.HTML, reply_markup=choose_action_button())


@admin_router.callback_query(F.data == "cancel_action")
async def cancel_action(callback: CallbackQuery):
    text = (f'Дію відхилено.\n' + footer())
    await callback.message.edit_text(text=text, reply_markup=choose_action_button())
