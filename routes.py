from aiogram import Router
from aiogram.types import Message, CallbackQuery, URLInputFile, ReplyKeyboardRemove

import data
from commands import SHOWS_COMMAND
from keyboards import tv_shows_keyboard_markup, TVShowsCallback
from models import TVShowModel


shows_router = Router()


@shows_router(SHOWS_COMMAND)
async def get_shows(message: Message):
    shows = data.get_shows()
    keyboard = tv_shows_keyboard_markup(shows)
    await message.answer(
        text="Shows list",
        reply_markup=keyboard
    )

@shows_router.callback_query(TVShowsCallback.filter())
async def get_show(callback: CallbackQuery, callback_data: TVShowsCallback):
    show_data = data.get_shows(callback_data.id)
    show = TVShowModel(**show_data)
    text = f"""
    Show: {show.name}
    Description: {show.description}
    Rating: {show.rating}
    Genre: {show.genre}
    Actors: {', '.join(show.actors)}
    """
    await callback.message.answer_photo(
        caption=text,
        photo=URLInputFile(
            url=show.poster,
            filename=show.name
        ),
        reply_markup=ReplyKeyboardRemove()
    )