from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup


def home_button() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(text="🏠Головне меню", callback_data="home")
    builder.adjust(2)
    return builder


def back_button() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️Назад", callback_data="back")
    builder.attach(home_button())
    builder.adjust(2)
    return builder


def choose_lang_button() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Українська", callback_data="lang_uk")
    builder.button(text="Русский", callback_data="lang_ru")
    return builder.as_markup()


def choose_brand_buttons(brands, brand_ids) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for brand, brand_id in zip(brands, brand_ids):
        builder.button(text=brand, callback_data=f"brand_{brand_id}")
    builder.adjust(2)
    return builder.as_markup()


def choose_category_buttons(types, type_ids) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for type, type_id in zip(types, type_ids):
        builder.button(text=type, callback_data=f"type_{type_id}")
    builder.button(text="Коди помилок котлів", callback_data="error")
    builder.adjust(2, 1)
    builder.attach(back_button())
    return builder.as_markup()


def choose_error_buttons(errors, error_ids) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for error, error_id in zip(errors, error_ids):
        builder.button(text=error, callback_data=f"error_{error_id}")
    builder.adjust(4)
    builder.attach(back_button())
    return builder.as_markup()


def choose_model_buttons(models, models_id) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for model, model_id in zip(models, models_id):
        builder.button(text=model, callback_data=f"model_{model_id}")
    builder.adjust(2)
    builder.attach(back_button())
    return builder.as_markup()


def choose_instructions_buttons(instructions, instruction_ids) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for instruction, instruction_id in zip(instructions, instruction_ids):
        builder.button(text=instruction, callback_data=f"instr_{instruction_id}")
    builder.adjust(1)
    builder.attach(back_button())
    return builder.as_markup()


def fill_form_keyboard(main_router: bool) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Подати заяву на фахівця", callback_data=f"role_spec")
    builder.adjust(1)
    builder.attach(back_button()) if main_router else builder.attach(home_button())
    return builder.as_markup()


def payment_keyboard(amount: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=f"Подякувати за {amount}️️ ⭐️", pay=True)
    builder.adjust(1)
    return builder.as_markup()


def change_info_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=f"Змінити інформацію", callback_data=f"change_info_user")
    builder.adjust(1)
    builder.attach(home_button())
    return builder.as_markup()


def select_column_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=f"ПІБ", callback_data=f"change_fullname")
    builder.button(text=f"Номер телефону", callback_data=f"change_phone")
    builder.button(text=f"Місто", callback_data=f"change_city")
    builder.adjust(1)
    builder.attach(home_button())
    return builder.as_markup()