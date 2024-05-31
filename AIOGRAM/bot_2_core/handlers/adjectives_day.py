from random import choice

from aiogram import Router, F
from aiogram.types import Message

from AIOGRAM.bot_2_core.utils.Adjectives_ru import adjectives_list
from AIOGRAM.bot_2_core.filters.word_filter import WordFilter

router = Router()
word_list = ["какой"]
router.message.filter(WordFilter(word_list))




@router.message(F.text, WordFilter([" я$", " я "]))
async def get_compliment(message: Message):
    phrases = [
        f"@{message.from_user.username} cегодня ты {choice(adjectives_list).lower()}",
        f"Сегодня у нас @{message.from_user.username} {choice(adjectives_list).lower()}",
        f"Приветствуем @{message.from_user.username} {choice(adjectives_list).lower()}"
    ]
    await message.reply(choice(phrases))

@router.message(F.text, WordFilter(["день"]))
async def get_compliment(message: Message):
    phrases = [
        f"Сегодня пятница, но это статическоее сообщение, и завтра будет пятница =)"]
    await message.reply(choice(phrases))



