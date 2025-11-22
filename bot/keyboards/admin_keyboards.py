from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

from bot.keyboards.main_keyboards import home_button
from bot.keyboards.registration_keyboards import all_areas


def choose_see_forms_button() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(text="Переглянути анкети", callback_data="action_see_forms")
    builder.adjust(1)
    return builder


def choose_action_button() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Кількість юзерів", callback_data="action_count_users")
    builder.button(text="Переглянути спеціалістів", callback_data="action_check_spec")
    builder.button(text="Переглянути анкети", callback_data="action_see_forms")
    builder.button(text="Редагувати товари", callback_data="action_edit_data")
    builder.attach(choose_see_forms_button())
    builder.button(text="Розіслати повідомлення", callback_data="action_send_messages")
    builder.adjust(1)
    builder.attach(home_button())
    return builder.as_markup()


def choose_answer_spec_button(user_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Підтвердити", callback_data=f"answer_confirm_{user_id}")
    builder.button(text="Відхилити", callback_data=f"answer_cancel_{user_id}")
    builder.adjust(2)
    return builder.as_markup()


def choose_after_form_button() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Обробити наступну заяву", callback_data=f"action_see_forms")
    builder.adjust(1)
    return builder.as_markup()


def choose_action_edit_button() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Додати", callback_data=f"add")
    builder.button(text="Редагувати", callback_data=f"add")
    builder.button(text="Видалити", callback_data=f"delete")
    builder.adjust(1)
    return builder.as_markup()


def choose_edit_data_button() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Бренд", callback_data=f"data_brand")
    builder.button(text="Тип обладнання", callback_data=f"data_type")
    builder.button(text="Помилка", callback_data=f"data_error")
    builder.button(text="Модель", callback_data=f"data_model")
    builder.button(text="Інструкція", callback_data=f"data_instruction")
    builder.adjust(2, 1)
    return builder.as_markup()


def choose_brand_button(brands, brand_ids) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for brand, brand_id in zip(brands, brand_ids):
        builder.button(text=brand, callback_data=f"brand_{brand_id}_{brand}")
    builder.adjust(2)
    return builder.as_markup()


def choose_type_button(types, type_ids) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for type, type_id in zip(types, type_ids):
        builder.button(text=type, callback_data=f"type_{type_id}_{type}")
    builder.adjust(1)
    return builder.as_markup()


def choose_model_buttons(models, models_id) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for model, model_id in zip(models, models_id):
        builder.button(text=model, callback_data=f"model_{model_id}_{model}")
    builder.adjust(2)
    return builder.as_markup()


def choose_error_buttons(errors, error_ids) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for error, error_id in zip(errors, error_ids):
        builder.button(text=error, callback_data=f"error_{error_id}_{error}")
    builder.adjust(4)
    return builder.as_markup()


def choose_instructions_buttons(instructions, instruction_ids) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for instruction, instruction_id in zip(instructions, instruction_ids):
        builder.button(text=instruction, callback_data=f"instr_{instruction_id}_{instruction}")
    builder.adjust(1)
    return builder.as_markup()


def choose_skip_button() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text="Пропустити")
    return builder.as_markup(resize_keyboard=True)


def choose_group_persons_buttons() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Усі юзери", callback_data="role_user")
    builder.button(text="Тільки фахівці", callback_data="role_spec")
    builder.adjust(1)
    return builder.as_markup()


def confirm_add_product_buttons() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='Підтвердити', callback_data='confirm_edit_product')
    builder.button(text='Відхилити', callback_data='cancel_action')
    builder.adjust(1)
    return builder.as_markup()


def next_step_button() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(text="Далі", callback_data="go_next_step")
    builder.adjust(1)
    return builder


def choose_volume_selected() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(text="Вибрати усі області", callback_data="select_all")
    builder.button(text="Очистити вибір", callback_data="clear_selection")
    builder.adjust(1)
    return builder


def choose_group_specialists_button(selected: list[str]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    categories = ["Монтажник", "Продавець-консультант", "Сервісант"]
    for category in categories:
        text = f"{'✅' if category in selected else '☐'} {category}"
        builder.button(text=text, callback_data=f"admincategory_{category}")
    builder.adjust(1)
    builder.attach(next_step_button())
    return builder.as_markup()


def choose_area_buttons(selected: list[str]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for area in all_areas:
        label = f"{'✅' if area in selected else '☐'} {area}"
        builder.button(text=label, callback_data=f"adminarea_{area}")
    builder.adjust(4)
    builder.attach(choose_volume_selected())
    builder.attach(next_step_button())
    return builder.as_markup()


def confirm_send_messages_buttons() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='Підтвердити', callback_data='confirm_send_messages')
    builder.button(text='Відхилити', callback_data='cancel_action')
    builder.adjust(1)
    return builder.as_markup()



