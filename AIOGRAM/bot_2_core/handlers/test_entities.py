from random import choice

from aiogram import Router, F
from aiogram.types import Message


from AIOGRAM.bot_2_core.filters.word_filter import WordFilter

router = Router()
word_list = ["смотри"]
router.message.filter(WordFilter(word_list))


@router.message(F.text)
async def entities_test(message: Message):
    entities = message.entities
    print(entities)


    await message.reply(f"Чек {}")
