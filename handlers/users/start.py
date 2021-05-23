from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp
from states.users import State
from utils.db_api.db_commands import create_new_user, check_user_in_database


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    if not await check_user_in_database(message.from_user.id):
        await message.answer(f"{message.from_user.full_name}!"
                             f'Введите код активации, чтобы я мог '
                             f'с вами продолжить сотрудничество!')
        await State.newbee.set()
    else:
        await State.user.set()

