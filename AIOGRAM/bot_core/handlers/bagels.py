import random
from re import match
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from ..utils.statesbagels import StepsBagels
from ..keyboards.reply import game_quit


NUM_DIGITS = 3  # Количество цифр в загаданном числе
MAX_GUESSES = 10  # количество попыток

def get_secret_num():
    """Возвращает NUM_DIGITS уникальных случайных цифры."""
    numbers = list('0123456789')  # Create a list of digits 0 to 9.
    random.shuffle(numbers)  # Shuffle them into random order.

    # Возвращает первые N цифр последоваательности
    secretNum = ''
    for i in range(NUM_DIGITS):
        secretNum += str(numbers[i])
    return secretNum

def num_valid(str_to_check):
    pre = "{" + str(NUM_DIGITS) + "}" #Пока хз как по другому вставить { и } в форматируемую строку ?/
    pattern = r"\b\d{}\b".format(pre)

    if match(pattern, str_to_check):
        return True

    return False

def repeat_num(str_to_check):
    check_dict = dict()
    for i in range(10):
        check_dict[i] = 0
    for num in str_to_check:
        check_dict[int(num)] += 1
        if check_dict[int(num)] > 1:
            return False
    return True


def get_clues(guess, secretnum):
    """Возвращает сроку содержащую  "Близко", "Попал", "Неудача" подсказки для догатки."""

    clues = []

    for i in range(len(guess)):
        if guess[i] == secretnum[i]:
            # Угаданнное число на своем месте.
            clues.append('Попал')
        elif guess[i] in secretnum:
            # Угаданное число не на своем месте
            clues.append('Близко')
    if len(clues) == 0:
        return 'Неудача'  # Не угадал ни одного числа
    else:
        # Отсортируйте подсказки в алфавитном порядке, чтобы их первоначальный порядок
        # не выдает информацию.
        clues.sort()
        # Создаем строку из списка
        return ' '.join(clues)

async def start_game(message: Message, state: FSMContext):
    await message.answer(f'''Bagels, логическая игра		
Я задумал {NUM_DIGITS}-х значное число. Цифры не повторяються.		
Попробуй его отгадать?		
Если я скажу:     Это будет значить:		
  Близко         Одно число верное но стоит не на своем месте.		
  Попал         Одно число верное и оно стоит на своем месте.		
  Неудача       Нет ни одного совпадения.		
У вас будет {MAX_GUESSES} попыток.

Для примера если я загодаю число 248 и твоя попытка будет 843, результат будет 
Попал Близко.''', reply_markup=game_quit)

    await state.update_data(secretnum=get_secret_num())
    await state.update_data(guesses=MAX_GUESSES)
    await state.set_state(StepsBagels.ATTEMPT_GUESS)

async def attemp_guess(message: Message, state: FSMContext):
    context_data = await state.get_data()
    secretnum = context_data.get("secretnum")
    guesses = context_data.get("guesses") - 1
    # await message.answer(f"{secretnum}")

    """Экстренная остановка игры"""
    if match(r"\b[QqSsCcСс]", message.text):
        await message.answer("Игра завершена")
        await state.clear()
        return


    """Завершение попыток"""
    if guesses == 0:
        await message.answer("Все попытки закончились\r\n"
                             "Хотите сыграть еще раз? (Да или Нет)")
        await state.set_state(StepsBagels.PLAY_AGAIN)
        return
    await state.update_data(guesses=guesses)

    """Проверка попытки"""
    if num_valid(message.text):
        if repeat_num(message.text):
            if message.text == secretnum:
                await message.answer(f"Победа, отгаданное число - {secretnum}")
                await message.answer(f"Хотите сыграть еще раз? (Да или Нет)")
                await state.set_state(StepsBagels.PLAY_AGAIN)
            else:
                result_mess = get_clues(message.text, secretnum)
                await message.answer(result_mess + f"\r\nУ вас осталось попыток: {guesses}", reply_markup=game_quit)
        else:
            await message.answer(f"Цифры не должны повторяться\r\nУ вас осталось попыток: {guesses}", reply_markup=game_quit)

    else:
        await message.answer(f"Нужно указать {NUM_DIGITS}-х значное число\r\nУ вас осталось попыток: {guesses}", reply_markup=game_quit)

async def play_again(message: Message, state: FSMContext):
    if match(r"\b[yYдД]", message.text):
        await start_game(message, state)
    else:
        await message.answer("Игра завершена")
        await state.clear()
