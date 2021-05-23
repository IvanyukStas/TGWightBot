from aiogram import types

from handlers.users.start import bot_start
from loader import dp
from states.users import State
from utils.db_api.db_commands import create_new_user, update_user_weight, check_user_weight_today, \
    check_user_in_database, create_user_weight


@dp.message_handler(state=None)
async def check_and_write(message: types.Message):
    if await check_user_in_database(message.from_user.id):
        await State.user.set()
        print('вызываю хандл со состоянием юзер')
        await bot_echo(message)
    else:
        await bot_start(message)

@dp.message_handler(state=State.newbee)
async def check_activation_code(message: types.Message):
    if message.text == '123':
        await create_new_user(message.from_user.full_name, message.from_user.id)
        await message.answer(f'Поздравляю, теперь мы можем с тобой начать записывать вес!')
        await State.user.set()
    else:
        await message.answer(f'К сожалению код не подходит('
                             f'Уточните код активации')


@dp.message_handler(state=State.user)
async def bot_echo(message: types.Message):
    if not message.text.isdigit():
        await message.answer(f"Чертило не тупи, напиши свой вес цифрами!!!!!")
        await message.answer(f"Сообщение:\n"
                             f"{message.text}")
    else:
        print('Пришло число проверяем, записан вес сегодня или нет?')
        if not await check_user_weight_today(message.from_user.id):
            await create_user_weight(message.text, message.from_user.id)
            await message.answer(f'Мы хаписали ваш вес - {message.text}\n'
                                 f'Чтобы узнать средний вес за 7 дней нажмите /7\n'
                                 f'За 28 дней /28')
        else:
            await update_user_weight(message.text, message.from_user.id)
            await message.answer(f'Мы хаписали ваш вес - {message.text}\n'
                                 f'Чтобы узнать средний вес за 7 дней на;мите /7\n'
                                 f'За 28 дней /28')