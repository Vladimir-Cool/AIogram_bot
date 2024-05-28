from aiogram.fsm.state import StatesGroup, State

class StepsBagels(StatesGroup):
    ATTEMPT_GUESS = State()
    PLAY_AGAIN = State()