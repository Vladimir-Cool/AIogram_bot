from aiogram import Router, F
from aiogram.types import Message

from AIOGRAM.bot_2_core.filters.word_filter import WordFilter

router = Router()
router.message.filter(WordFilter([""]))


