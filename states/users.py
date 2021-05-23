from aiogram.dispatcher.filters.state import StatesGroup, State


class State(StatesGroup):
    newbee = State()
    user = State()