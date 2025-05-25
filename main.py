import os
import logging
import sys
import asyncio

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import CommandStart
from aiogram.types import Message


from routes import shows_router
from commands import COMMANDS, SHOWS_COMMAND


load_dotenv()

TBOT = os.getenv("TBOT")
dp = Dispatcher()
dp.include_routers(shows_router)


@dp.message(CommandStart())
async def command_start(message: Message):
    await message.answer(text=f"Hello, {message.from_user.full_name}!")

async def main():
    bot = Bot(token=TBOT, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await bot.set_my_commands(COMMANDS)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
        