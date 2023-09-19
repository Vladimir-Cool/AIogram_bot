from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command="start",
            description="Начало работ"
        ),
        BotCommand(
            command="start_bagels",
            description="Начать игру bagels"
        ),
        BotCommand(
            command="start_black_jack",
            description="Начать игру BlackJack"
        ),
        BotCommand(
            command="help",
            description="Помощь"
        ),
        BotCommand(
            command="form",
            description="Начать опрос"
        )
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())
