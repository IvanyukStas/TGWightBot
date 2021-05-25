from functools import reduce

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery

from handlers.users.start import bot_start
from keyboards.inline.user_keyboards import average_weight_keyboard
from loader import dp
from states.users import States
from utils.db_api.db_commands import create_new_user, update_user_weight, check_user_weight_today, \
    check_user_in_database, create_user_weight, wieght_data


#@dp.message_handler(commands=['7'], commands_prefix='/', state=States.user)
@dp.callback_query_handler(lambda c: c.data == "average7", state=States.user)
async def average_weight_7(call: CallbackQuery):
    data = await wieght_data(call.from_user.id)
    data = {u.date_of_update.date(): u.user_weight for u in data}
    sorted_data = sorted(data.items(), reverse=True)[:7]
    sum_data = sum(int(i[1]) for i in sorted_data)
    if len(data) > 6:
        await call.answer(f'Ваш средний вес за 7 дней - {sum_data}')
    else:
        await call.answer(f'Ваш средний вес за последние {len(data)} дней - {sum_data}')
        await call.from_user.id

@dp.message_handler(commands=['28'], commands_prefix='/', state=States.user)
async def average_weight_7(message: types.Message):
    data = await wieght_data(message.from_user.id)
    data = {u.date_of_update.date(): u.user_weight for u in data}
    sorted_data = sorted(data.items(), reverse=True)[:28]
    sum_data = sum(int(i[1]) for i in sorted_data)
    if len(data) > 27:
        await message.answer(f'Ваш средний вес за 28 дней - {sum_data}')
    else:
        await message.answer(f'Ваш средний вес за последние {len(data)} дней - {sum_data}')


@dp.message_handler(state=None)
async def check_and_write(message: types.Message):
    if await check_user_in_database(message.from_user.id):
        await States.user.set()
        await bot_echo(message)
    else:
        await bot_start(message)

@dp.message_handler(state=States.newbee)
async def check_activation_code(message: types.Message):
    if message.text == '123':
        await create_new_user(message.from_user.full_name, message.from_user.id)
        await message.answer(f'Поздравляю, теперь мы можем с тобой начать записывать вес!')
        await States.user.set()
    else:
        await message.answer(f'К сожалению код не подходит('
                             f'Уточните код активации')


@dp.message_handler(state=States.user)
async def bot_echo(message: types.Message):
    if not message.text.isdigit():
        await message.answer(f"Введите ваш вес цифрами без использования каких либо букв!")
    else:
        if not await check_user_weight_today(message.from_user.id):
            await create_user_weight(message.text, message.from_user.id)
            await message.answer(f'Мы хаписали ваш вес - {message.text}\n'
                                 f'Чтобы узнать средний вес за 7 дней нажмите /7\n'
                                 f'За 28 дней /28')
        else:
            await update_user_weight(message.text, message.from_user.id)
            await message.answer(f'Мы изменили ваш предыдущий вес - {message.text}\n'
                                 f'Чтобы узнать средний вес за 7 дней нажмите /7\n'
                                 f'За 28 дней /28', reply_markup=average_weight_keyboard)


