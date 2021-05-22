from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp
from utils.db_api.db_commands import create_new_user


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}!"
                         f'Для меню жми /menu')
    await create_new_user(message.from_user.full_name, message.from_user.id)
