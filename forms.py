from aiogram.fsm.state import State, StatesGroup

class ShowForm(StatesGroup):
    name = State()
    description = State()
    rating = State()
    genre = State()
    actors = State()
    poster = State()
    # video = State()
    # year = State()
    # country = State()
    # seasons = State()
    # episodes = State()