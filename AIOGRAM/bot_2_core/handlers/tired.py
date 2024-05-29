import re
from aiogram import Router, F
from aiogram.types import Message

from AIOGRAM.bot_2_core.filters.word_filter import WordFilter

route = Router()
word_list = ["устал", "надоел", "замучил",]
route.message.filter(WordFilter(word_list))

@route.message(F.text)
async def is_tired(message: Message):
    await message.reply("Не отчаивайся у тебя все получится, скоро домой и там ты отдохнешь!!")

