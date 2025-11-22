from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InputMediaPhoto
from aiogram.types.input_file import BufferedInputFile

from create_bot import s3
from bot.keyboards.main_keyboards import back_button


async def send_navigation_message(message: Message):
    text = 'Оберіть наступну дію:'
    markup = back_button().as_markup()
    await message.answer(text=text, parse_mode=ParseMode.HTML, reply_markup=markup)


def start_message(registered: bool) -> str:
    text = f'Доброго часу доби!😊\nБот допомогає отримати інформацію про газове обладнання.\n'
    if registered:
        text += f'Оберіть марку:'
    else:
        text += (f'Для користування ботом потрібно зареєструватися.\n'
                 f'Оберіть роль:')
    return text


def build_prompt(description: str | None, *lines: str) -> str:
    parts = []
    if description:
        desc = description.strip()
        if desc:
            parts.append(desc)
    parts.extend(line for line in lines)
    return '\n'.join(parts)


async def send_prompt(message: Message, state: FSMContext, fetch_fn, *args: int,
                      keyboard_fn, photo_path: str | None, text: str, next_state: str):
    items = await fetch_fn(*args)
    if not items:
        text += (f'На жаль тут зараз нічого немає.🙁\n'
                 f'У найближчому майбутньому ми доповнемо цей розділ.📝')
        markup = back_button().as_markup()
    else:
        markup = keyboard_fn(
            [i[0] for i in items],
            [i[1] for i in items]
        )

    if photo_path is not None:
        file_to_send = await get_document_from_s3(photo_path)
        media = InputMediaPhoto(media=file_to_send, caption=text, parse_mode=ParseMode.HTML)
        await message.edit_media(media=media, reply_markup=markup)
    else:
        await message.edit_caption(caption=text, reply_markup=markup, parse_mode=ParseMode.HTML)
    await state.set_state(next_state)


async def get_document_from_s3(file: str) -> BufferedInputFile:
    file_data = await s3.download_file(file)
    file_to_send = BufferedInputFile(
        file=file_data,
        filename=file
    )
    return file_to_send


def render_data(data: dict) -> str:
    labels = {
        'item': 'Продукт',
        'brand_name': 'Бренд',
        'category_name': 'Тип обладнання',
        'model_name': 'Модель',
        'title': 'Назва',
        'description': 'Опис',
        'role': 'Рівень доступу',
        'delete_name': 'Назва',
        'fullname': 'ПІБ',
        'area': 'Область',
        'phone': 'Номер телефону',
        'city': 'Місто',
        'category': 'Галузь праці',
    }

    lines = ['Інформація:']
    for key, val in data.items():
        # Пропускаем, если нет метки или значение пустое/None
        if key not in labels or val is None:
            continue

        pretty_key = labels[key]
        lines.append(f'<b>{pretty_key}</b>: {val}')
    return '\n'.join(lines)
