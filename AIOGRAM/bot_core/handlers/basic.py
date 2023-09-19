from aiogram import Bot
from aiogram.types import Message

from ..keyboards.reply import reply_keyboard, loc_tel_poll_keyboard, get_reply_keyboard


async def get_start(message: Message, bot: Bot, counter: str):
    await message.answer(f"Сообщение №{counter}")
    # await message.answer(f"Привет {message.from_user.first_name}. это 'answer'.",
    #                      reply_markup=get_reply_keyboard())
    await message.answer(f"Привет {message.from_user.first_name}. это 'answer'.")


async def get_location(message: Message, bot: Bot):
    await message.answer("Ты отправил локацию\r\a"
                         f"{message.location.latitude}\r\n{message.location.longitude}")


async def get_photo(message: Message, bot: Bot):
    await message.answer("Отлично. Ты отправил картнку, я ее сохраню.")
    file = await bot.get_file(message.photo[-1].file_id)
    await bot.download_file(file.file_path, "photo.jpg")


async def get_hello(message: Message, bot: Bot):
    await message.answer("И тебе привет!")

async def get_help(message: Message, bot: Bot):
    await message.answer(f"{message.from_user.first_name}, помощь пока не реализованна, придеться самому как то справляться, держись!")
