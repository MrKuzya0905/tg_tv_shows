from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, URLInputFile, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

import data
from commands import SHOWS_COMMAND, ADD_SHOW_COMMAND
from keyboards import tv_shows_keyboard_markup, TVShowsCallback, del_tv_show_keyboard
from models import TVShowModel
from forms import ShowForm


shows_router = Router()


@shows_router.message(SHOWS_COMMAND)
async def get_shows(message: Message):
    shows = data.get_shows()
    keyboard = tv_shows_keyboard_markup(shows)
    await message.answer(
        text="Shows list",
        reply_markup=keyboard
    )


@shows_router.callback_query(TVShowsCallback.filter())
async def get_show(callback: CallbackQuery, callback_data: TVShowsCallback):
    show_data = data.get_shows(show_id=callback_data.id)
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
        reply_markup=del_tv_show_keyboard(callback_data.id)
    )


@shows_router.message(ADD_SHOW_COMMAND)
async def add_show(message: Message, state: FSMContext):
    """
    Description of add_show

    Args:
        message (Message):
        state (FSMContext):

    """
    await state.set_state(ShowForm.name)
    await message.answer(
        text="Please enter the name of the show:",
        reply_markup=ReplyKeyboardRemove()
    )


@shows_router.message(ShowForm.name)
async def get_show_name(message: Message, state: FSMContext):
    """
    Description of get_show_name

    Args:
        message (Message):
        state (FSMContext):

    """
    await state.update_data(name=message.text)
    await state.set_state(ShowForm.description)
    await message.answer(
        text="Please enter the description of the show:",
        reply_markup=ReplyKeyboardRemove()
    )


@shows_router.message(ShowForm.description)
async def get_show_description(message: Message, state: FSMContext):
    """
    Description of get_show_description

    Args:
        message (Message):
        state (FSMContext):

    """
    await state.update_data(description=message.text)
    await state.set_state(ShowForm.rating)
    await message.answer(
        text="Please enter the rating of the show(imdb):",
        reply_markup=ReplyKeyboardRemove()
    )


@shows_router.message(ShowForm.rating)
async def get_show_rating(message: Message, state: FSMContext):
    await state.update_data(rating=float(message.text))
    await state.set_state(ShowForm.genre)
    await message.answer(
        text="Please enter the genre of the show:",
        reply_markup=ReplyKeyboardRemove()
    )


@shows_router.message(ShowForm.genre)
async def get_show_genre(message: Message, state: FSMContext):
    await state.update_data(genre=message.text)
    await state.set_state(ShowForm.actors)
    await message.answer(
        text="Please enter the actors of the show (comma separated):",
        reply_markup=ReplyKeyboardRemove()
    )


@shows_router.message(ShowForm.actors)
async def get_show_actors(message: Message, state: FSMContext):
    actors = [actor.strip() for actor in message.text.split(",")]
    await state.update_data(actors=actors)
    await state.set_state(ShowForm.poster)
    await message.answer(
        text="Please send url of the poster of the show:",
        reply_markup=ReplyKeyboardRemove()
    )

@shows_router.message(ShowForm.poster)
async def get_show_poster(message: Message, state: FSMContext):
    show_data = await state.update_data(poster=message.text)
    data.add_show(show_data)
    await state.clear()
    await message.answer(
        text=f"Show '{show_data["name"]}'added successfully!",
        reply_markup=ReplyKeyboardRemove()
    )

@shows_router.callback_query(F.data.startswith("del_show_"))
async def del_show(callback: CallbackQuery, state: FSMContext):
    show_id = int(callback.data.split("_")[-1])
    show = data.get_shows(show_id=show_id)
    data.delete_show(show_id)
    await callback.message.answer(
        text=f"Show '{show.get("name")}' deleted successfully!"
    )
    