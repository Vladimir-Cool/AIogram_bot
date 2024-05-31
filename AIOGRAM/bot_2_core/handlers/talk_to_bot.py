from random import choice

from aiogram import Router

from AIOGRAM.bot_2_core.filters.word_filter import WordFilter
from AIOGRAM.bot_2_core.handlers.adjectives_day import router as adj_router
from AIOGRAM.bot_2_core.handlers.test_entities import router as test_router


router = Router()
word_list = ["^бот"]
router.message.filter(WordFilter(word_list))

router.include_routers(adj_router, test_router)
