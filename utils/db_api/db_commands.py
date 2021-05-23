from aiogram import types

from utils.db_api.models import User, Weight
from datetime import datetime


async def update_weight(message):
    return await User.query.order_by(User.user_name).all()

async def add_item(**kwargs):
    new_item = await User(**kwargs).create()
    return new_item

async def create_new_user(user_name, user_tg_id):
    print('Начинаю')
    user = await User.create(user_name=user_name, user_tg_id=user_tg_id)
    print('Кончаю')

async def create_user_weight(user_weight, user_tg_id):
    print('Начинаю запись веса')
    user = await Weight.create(user_weight=user_weight, users_id=user_tg_id)
    print('Вес записан')

async def check_user_weight_today(user_tg_id):
    user_weight = await Weight.query.where(Weight.users_id == user_tg_id).gino.all()
    date_now = datetime.utcnow()
    for u in user_weight:
        if date_now.day == u.date_of_update.day and date_now.month == u.date_of_update.month:
            print('check_user_weight_today --- True')
            return True
    print('check_user_weight_today --- False')
    return False


async def update_user_weight(user_message, user_tg_id):
    user = await Weight.query.where(Weight.users_id == user_tg_id).gino.all()
    for u in user:
        print('проверяю дату создания')
        date_now = datetime.utcnow()
        if date_now.day == u.date_of_update.day and date_now.month == u.date_of_update.month:
            await u.update(user_weight=user_message).apply()
            break

async def check_user_in_database(user_tg_id):
    user = await User.query.where(User.user_tg_id == user_tg_id).gino.first()
    if user:
        print('юзер есть')
        return True
    else:
        print('юзера нет')
        return False

async def wieght_data(user_tg_id):
    user = await Weight.query.where(Weight.users_id == user_tg_id).gino.all()
    return user
