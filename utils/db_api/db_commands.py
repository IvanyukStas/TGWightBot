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
    print('Начинаю')
    user = await Weight.create(user_weight=user_weight, users_id=user_tg_id)
    print('Кончаю')


async def update_user_weight(user_tg_id, user_message):
    #user = await Weight.select('user_weight').where(User.user_tg_id == user_tg_id).gino.scalar()
    user = await Weight.query.where(Weight.users_id == user_tg_id).gino.all()
    for u in user:
        delta = user[0].date_of_update - datetime.utcnow()
        if delta.days < 0:
            await u.update(user_weight=user_message).apply()
            break
        delta = u.date_of_update - datetime.utcnow()
        print(delta.days)
        if int(delta.days) < 0:
            print(u.date_of_update)
            await u.update(user_weight=user_message).apply()
            break
