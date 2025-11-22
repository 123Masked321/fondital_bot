import asyncio

from bot.middlewares.database_session import DbSessionMiddleware
from create_bot import bot, dp

from bot.handlers.user.prolife import profile_router
from bot.handlers.user.user_router import user_router
from bot.handlers.admin.admin_router import admin_router
from bot.handlers.user.registration import registration_router
from bot.handlers.user.start import start_router
from bot.handlers.admin.add_product_router import add_product_router
from bot.handlers.admin.delete_product_router import delete_product_router
from bot.handlers.user.payment import payment_router

from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands():
    commands = [
        BotCommand(command="start", description="Старт"),
        BotCommand(command="profile", description="Профіль"),
        BotCommand(command="donate", description="Підтримати проєкт"),
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


async def main():
    dp.include_router(admin_router)
    dp.include_router(add_product_router)
    dp.include_router(delete_product_router)
    dp.include_router(user_router)
    dp.include_router(registration_router)
    dp.include_router(start_router)
    dp.include_router(profile_router)
    dp.include_router(payment_router)

    dp.message.middleware(DbSessionMiddleware)
    dp.callback_query.middleware(DbSessionMiddleware)

    await set_commands()

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
