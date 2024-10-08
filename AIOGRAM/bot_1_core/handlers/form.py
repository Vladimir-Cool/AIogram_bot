from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from ..utils.statesform import StepsForm


async def get_form(message: Message, state: FSMContext):
    await message.answer(f"{message.from_user.first_name}, начинаем заполнять анкету. Введите свое имя")
    await state.set_state(StepsForm.GET_NAME)


async def get_name(message: Message, state: FSMContext):
    await message.answer(f"Твое имя:\r\n{message.text}\r\nТеперь введите фамилию")
    await state.update_data(name=message.text)
    await state.set_state(StepsForm.GET_LAST_NAME)


async def get_last_name(message: Message, state: FSMContext):
    await message.answer(f"Твоя фамилия:\r\n{message.text}\r\nТеперь введите сколько вам лет")
    await state.update_data(last_name=message.text)
    await state.set_state(StepsForm.GET_AGE)


async def get_age(message: Message, state: FSMContext):
    await message.answer(f"Твой возвраст:\r\n{message.text}\r\n")
    await state.update_data(age=message.text)
    context_data = await state.get_data()
    await message.answer(f"Сохраненные данные в машине состояний:\r\n{str(context_data)}")
    name = context_data.get("name")
    last_name = context_data.get("last_name")
    age = context_data.get("age")
    data_user = f"Вот твои данные\r\n" \
                f"Имя {name}\r\n" \
                f"Фамилия {last_name}\r\n" \
                f"Возраст {age}" \

    await message.answer(data_user)
    await state.clear()

