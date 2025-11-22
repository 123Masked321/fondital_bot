from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup


all_areas = [
    "Вінницька", "Волинська", "Донецька", "Житомирська", "Закарпатська",
    "Запорізька", "Івано-Франківська", "Київська", "Кіровоградська",
    "Луганська", "Львівська", "Миколаївська", "Одеська", "Полтавська",
    "Рівненська", "Сумська", "Тернопільска", "Харківська", "Херсонська",
    "Хмельницька", "Черкаська", "Чернігівська", "Чернівецька", "Крим"
]


def choose_role_button() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Користувач", callback_data=f"role_user")
    builder.button(text="Фаховий спеціаліст", callback_data=f"role_spec")
    builder.adjust(2)
    return builder.as_markup()


def choose_area_button() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for area in all_areas:
        builder.button(text=area, callback_data=f"area_{area}")
    builder.adjust(5)
    return builder.as_markup()


def get_number_button() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text="Поділитися контактом", request_contact=True)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def choose_category_button() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Монтажник", callback_data=f"category_Монтажник")
    builder.button(text="Продавець-консультант", callback_data=f"category_Продавець-консультант")
    builder.button(text="Сервісант", callback_data=f"category_Сервісант")
    builder.adjust(1)
    return builder.as_markup()