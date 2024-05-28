from aiogram import F, Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters.command import Command

from AIOGRAM.bot_2_core.keyboards.yes_no_kb import yes_no_kb

router = Router()


@router.message(Command("test1"))
async def cmd_test1(message: Message):
    await message.reply("Test 1", reply_markup=yes_no_kb())


@router.message(F.text.lower() == "да")
async def answer_yes(message: Message):
    await message.answer(
        "Это здорово!",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(F.text.lower() == "нет")
async def answer_no(message: Message):
    await message.answer(
        "Жаль...",
        reply_markup=ReplyKeyboardRemove()
    )

