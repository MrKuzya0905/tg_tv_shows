from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

class TVShowsCallback(CallbackData, prefix="tv_shows", sep=";"):
    id: int
    name: str

def tv_shows_keyboard_markup(shows: list):
    builder = InlineKeyboardBuilder()
    for index, show in enumerate(shows):
        callback_data = TVShowsCallback(id=index, **show)
        builder.button(
            text=callback_data.name,
            callback_data=callback_data.pack()
        )

    builder.adjust(2, repeat=True)
    return builder.as_markup()

def del_tv_show_keyboard(show_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Delete Show",
        callback_data=f"del_show_{show_id}"
    )
    return builder.as_markup()
    