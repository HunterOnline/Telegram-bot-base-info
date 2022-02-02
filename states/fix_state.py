from aiogram.dispatcher.filters.state import StatesGroup, State


class FixMessage(StatesGroup):
    EnterQuestion = State()
    EnterAnswer = State()
    Confirm = State()


class Del(StatesGroup):
    DelQuestionAnswer = State()
