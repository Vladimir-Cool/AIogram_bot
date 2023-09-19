from aiogram import Bot
from aiogram.types import Message


async def get_true_contact(message: Message, bot: Bot):
    await message.answer("Ты отправил свой контакт")

async def get_false_contact(message: Message, bot: Bot):
    await message.answer("Ты отправил не свой контакт")