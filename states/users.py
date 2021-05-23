from aiogram.dispatcher.filters.state import StatesGroup, State


class States(StatesGroup):
    newbee = State()
    user = State()
    average = State()

