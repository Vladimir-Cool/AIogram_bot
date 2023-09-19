import random
from re import match

from bot_settings import bot

NUM_DIGITS = 3  # Количество цифр в загаданном числе
MAX_GUESSES = 10  # количество попыток


def print_chat(message, print_string):
    mess = print_string
    return bot.send_message(message.chat.id, mess, parse_mode="html")





def getSecretNum():
    """Возвращает NUM_DIGITS уникальных случайных цифры."""
    numbers = list('0123456789')  # Create a list of digits 0 to 9.
    random.shuffle(numbers)  # Shuffle them into random order.

    # Возвращает первые N цифр последоваательности
    secretNum = ''
    for i in range(NUM_DIGITS):
        secretNum += str(numbers[i])
    return secretNum


def getClues(guess, secretNum):
    """Возвращает сроку содержащую  "Близко", "Попал", "Неудача" подсказки для догатки."""
    if guess == secretNum:
        return 'Ты отгодал!'

    clues = []

    for i in range(len(guess)):
        if guess[i] == secretNum[i]:
            # Угаданнное число на своем месте.
            clues.append('Попал')
        elif guess[i] in secretNum:
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


def main_bagels(message):


    print_chat(message, f'''Bagels, логическая игра		
Я задумал {NUM_DIGITS}-х значное число		
Попробуй его отгадать?		
Если я скажу:     Это будет значить:		
  Близко         Одно число верное но стоит не на своем месте.		
  Попал         Одно число верное и оно стоит на своем месте.		
  Неудача       Нет ни одного совпадения.		

Для примера если я загодаю число 248 и твоя попытка будет 843, результат будет 
Попал Близко.''')

    while True:
        secretNum = getSecretNum()
        print_chat(message, 'Я загодал число.')
        print_chat(message, f' У тебя {MAX_GUESSES} попыток')

        numGuesses = 1
        while numGuesses <= MAX_GUESSES:
            guess = ''
            # Цикл проверки попыток
            while len(guess) != NUM_DIGITS or not guess.isdecimal():
                print_chat(message, f'Номер попытки #{numGuesses}: ')

                guess = read_chat(message)

            clues = getClues(guess, secretNum)
            print_chat(message, clues)
            numGuesses += 1

            if guess == secretNum:
                break  # Если отгодал то цикл завершается
            if numGuesses > MAX_GUESSES:
                print_chat(message, 'Ты потратил все попытки.')
                print_chat(message, f'Правильный ответ был {secretNum}.')

        # Ask player if they want to play again.
        print_chat(message, 'Хочешь сыграть снова? (yes or no)')
        if not input('> ').lower().startswith('y'):
            break
    print_chat(message, 'Спасибо за игру!')


# для запуска игры
# if __name__ == '__main__':
#     main_bagels()