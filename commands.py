from aiogram.filters import Command
from aiogram.types.bot_command import BotCommand

SHOWS_COMMAND = Command("tv_shows")
ADD_SHOW_COMMAND = Command("add_show")

COMMANDS = [
    BotCommand(command="tv_shows", description="Get TV shows list"),
    BotCommand(command="add_show", description="add a show to your list"),
]