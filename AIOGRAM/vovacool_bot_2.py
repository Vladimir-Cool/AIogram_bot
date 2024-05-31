import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, BotCommandScopeDefault
from aiogram.filters.command import Command

from settings import settings
from bot_2_core.handlers import test, different_types, dice_test, tired, talk_to_bot
# Включаем логирование, чтобы не пропустить важные сообщения


logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - [%(levelname)s] -  %(name)s - "
                            "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")


# Запуск процесса поллинга новых апдейтов
async def start():
    bot = Bot(token=settings.TOKEN2, parse_mode="HTML")
    await bot.set_my_commands([], BotCommandScopeDefault())

    # Диспетчер
    dp = Dispatcher()
    dp.include_routers(tired.router, talk_to_bot.router, different_types.router)


    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

