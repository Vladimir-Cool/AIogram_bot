from aiogram.fsm.state import StatesGroup, State

class StepsBlackJack(StatesGroup):
    MAKE_BET = State()
    GAME = State()
    PLAY_AGAIN = State()
