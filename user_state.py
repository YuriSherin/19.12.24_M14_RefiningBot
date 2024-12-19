from aiogram.dispatcher.filters.state import StatesGroup, State

class UserState(StatesGroup):
    AGE = State()       # возраст
    GROWTH = State()    # рост
    WEIGHT = State()    # вес
