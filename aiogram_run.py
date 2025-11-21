import asyncio
from create_bot import bot, dp, db
from handlers.prolife import profile_router
from handlers.user_router import user_router
from handlers.registration import registration_router
from handlers.start import start_router
from handlers.admin.admin_router import admin_router
from handlers.admin.add_product_router import add_product_router
from handlers.admin.delete_product_router import delete_product_router
from handlers.payment import payment_router
from aiogram.types import BotCommand, BotCommandScopeDefault


# Функция, которая настроит командное меню (дефолтное для всех пользователей)
async def set_commands():
    commands = [BotCommand(command='start', description='Старт'),
                BotCommand(command='profile', description='Переглянути профіль'),
                BotCommand(command='donate', description='Подяка проекту(тільки при бажанні)')]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


# Функция, которая выполнится когда бот запустится
async def start_bot():
    await set_commands()
    await db.connect()


# Функция, которая выполнится когда бот завершит свою работу
async def stop_bot():
    await db.close()


async def main():
    dp.include_router(admin_router)
    dp.include_router(add_product_router)
    dp.include_router(delete_product_router)
    dp.include_router(user_router)
    dp.include_router(registration_router)
    dp.include_router(start_router)
    dp.include_router(profile_router)
    dp.include_router(payment_router)

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())