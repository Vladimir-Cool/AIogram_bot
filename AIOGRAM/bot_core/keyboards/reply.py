from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonPollType
from aiogram.utils.keyboard import ReplyKeyboardBuilder


reply_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text="Ряд 1. Кнопка 1."
        ),
        KeyboardButton(
            text="Ряд 1. Кнопка 2."
        ),
        KeyboardButton(
            text="Ряд 1. Кнопка 3."
        ),
        KeyboardButton(
            text="Ряд 1. Кнопка 4."
        )
    ],
    [
        KeyboardButton(
            text="Ряд 2. Кнопка 1."
        ),
        KeyboardButton(
            text="Ряд 2. Кнопка 2."
        ),
        KeyboardButton(
            text="Ряд 2. Кнопка 3."
        )
    ],
    [
        KeyboardButton(
            text="Ряд 3. Кнопка 1."
        ),
        KeyboardButton(
            text="Ряд 3. Кнопка 2."
        )
    ]
], resize_keyboard=True, one_time_keyboard=True, input_field_placeholder="Выбирайте кнопку и нажимайте", selective=True)

loc_tel_poll_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text="Отправка геолокации",
            request_location=True
        ),
        KeyboardButton(
            text="Отправка контакта",
            request_contact=True
        ),
        KeyboardButton(
            text="Создать викторину",
            request_poll=KeyboardButtonPollType()
        )
    ]
], resize_keyboard=True, one_time_keyboard=False, input_field_placeholder="Отправить локацию, номер телефона или создать викторину/опрос")

game_quit = ReplyKeyboardMarkup(keyboard=[[
        KeyboardButton(
            text="quit",
            )
        ]
    ], resize_keyboard=True, one_time_keyboard=True
)

def get_reply_keyboard():
    keyboard_builder = ReplyKeyboardBuilder()

    keyboard_builder.button(text="Кнопка 1")
    keyboard_builder.button(text="Кнопка 2")
    keyboard_builder.button(text="Кнопка 3")
    keyboard_builder.button(text="Отправить геолокацию", request_location=True)
    keyboard_builder.button(text="Отправить Свой контакт", request_contact=True)
    keyboard_builder.adjust(3, 2, 1)
    return keyboard_builder.as_markup(resize_keyboard=True, one_time_keyboard=False, input_field_placeholder="Отправить локацию, номер телефона или создать викторину/опрос")
