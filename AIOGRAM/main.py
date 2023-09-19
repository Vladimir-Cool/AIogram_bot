from aiogram import Bot, Dispatcher, F
from aiogram.types import ContentType
import asyncio
import logging
from aiogram.filters import Command

from settings import settings
from bot_core.handlers.basic import get_start, get_photo, get_hello, get_location, get_help
from bot_core.handlers.contact import get_true_contact, get_false_contact
from bot_core.utils.statesform import StepsForm
from bot_core.handlers import form
from bot_core.utils.statesbagels import StepsBagels
from bot_core.handlers import bagels
from bot_core.utils.stateblackjack import StepsBlackJack
from bot_core.handlers import blackjack
from bot_core.filters.iscontact import IsTrueContact
from bot_core.utils.commands import set_commands
from bot_core.middlewares.counter import CounterMiddleware
from bot_core.middlewares.officehours import OfficeHoursMiddleware

async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(settings.bots.admin_id, text="Бот запущен")

async def stop_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text="Бот отключен")


async def start():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] -  %(name)s - "
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")


    bot = Bot(token=settings.bots.bot_token)
    dp = Dispatcher()
    dp.message.middleware.register(CounterMiddleware())
    # dp.message.middleware.register(OfficeHoursMiddleware())

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    dp.message.register(get_hello, F.text == "Привет")
    dp.message.register(get_location, F.location)
    dp.message.register(get_photo, F.photo)
    """Help"""
    dp.message.register(get_help, Command(commands=["help"]))
    """Form"""
    dp.message.register(form.get_form, Command(commands=["form"]))
    dp.message.register(form.get_name, StepsForm.GET_NAME)
    dp.message.register(form.get_last_name, StepsForm.GET_LAST_NAME)
    dp.message.register(form.get_age, StepsForm.GET_AGE)
    """Bagels"""
    dp.message.register(bagels.start_game, Command(commands=["start_bagels"]))
    dp.message.register(bagels.attemp_guess, StepsBagels.ATTEMPT_GUESS)
    dp.message.register(bagels.play_again, StepsBagels.PLAY_AGAIN)
    """Black Jack"""
    dp.message.register(blackjack.start_game, Command(commands=["start_black_jack"]))
    dp.message.register(blackjack.bet, StepsBlackJack.MAKE_BET)
    dp.message.register(blackjack.game, StepsBlackJack.GAME)


    # dp.message.register(get_true_contact, F.contact, IsTrueContact())
    dp.message.register(get_false_contact, F.contact)
    dp.message.register(get_start, Command(commands=["start", "run"]))

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start())