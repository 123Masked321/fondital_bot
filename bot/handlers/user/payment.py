from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery

from bot.keyboards.main_keyboards import payment_keyboard, home_button
from bot.middlewares.user_exist_middleware import UserExistMiddleware

payment_router = Router()
payment_router.message.middleware(UserExistMiddleware())

CURRENCY = 'XTR'


@payment_router.message(Command('donate'))
async def choose_amount(message: Message, is_registered: bool) -> None:
    if is_registered:
        text = 'Вкажіть суму (у ⭐️), яку ви бажаєте пожертвувати.'
        await message.answer(text=text, parse_mode=ParseMode.HTML, reply_markup=home_button().as_markup())


@payment_router.message(F.text)
async def choose_amount(message: Message) -> None:
    if message.text.isnumeric():
        prices = [LabeledPrice(label=CURRENCY, amount=int(message.text))]
        await message.answer_invoice(
            title='Підтримати бота',
            description=f'Підтримати бота за {message.text} ⭐️',
            prices=prices,
            provider_token='',
            payload='channel_support',
            currency=CURRENCY,
            reply_markup=payment_keyboard(int(message.text))
        )
    else:
        text = 'gfd'
        return


@payment_router.pre_checkout_query()
async def pre_checkout(query: PreCheckoutQuery) -> None:
    await query.answer(ok=True)


@payment_router.message(F.succesful_payment)
async def succesful_payment(message: Message) -> None:
    await message.answer('Дякуємо за підтримку проекта!')
