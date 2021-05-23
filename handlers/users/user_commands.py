from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from handlers.users.start import bot_start
from loader import dp
from states.users import  States
from utils.db_api.db_commands import create_new_user, update_user_weight, check_user_weight_today, \
    check_user_in_database, create_user_weight, wieght_data


@dp.message_handler(commands=['7'], commands_prefix='/', state=States.user)
async def average_weight_7(message: types.Message):
    await message.answer(f'Средний вес за 7 дней')
    data = await wieght_data(message.from_user.id)
    data = {u.date_of_update.date():u.user_weight for u in data}
    a = [i for i in data.keys()]
    a = sorted(a, reverse=True)[:7]
    print(a)
    print(data)



@dp.message_handler(commands=['28'], commands_prefix='/', state=States.user)
async def average_weight_7(message: types.Message):
    await message.answer(f'Средний вес за 28 дней')


@dp.message_handler(state=None)
async def check_and_write(message: types.Message):
    if await check_user_in_database(message.from_user.id):
        await States.user.set()
        print('вызываю хандл со состоянием юзер')
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
        print('Пришло число проверяем, записан вес сегодня или нет?')
        if not await check_user_weight_today(message.from_user.id):
            await create_user_weight(message.text, message.from_user.id)
            await message.answer(f'Мы хаписали ваш вес - {message.text}\n'
                                 f'Чтобы узнать средний вес за 7 дней нажмите /7\n'
                                 f'За 28 дней /28')
            #await States.average.set()
        else:
            await update_user_weight(message.text, message.from_user.id)
            await message.answer(f'Мы изменили ваш предыдущий вес - {message.text}\n'
                                 f'Чтобы узнать средний вес за 7 дней нажмите /7\n'
                                 f'За 28 дней /28')
            #await States.average.set()

