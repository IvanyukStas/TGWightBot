from utils.db_api.db_commands import add_item

import asyncio

from utils.db_api.database import create_db

# Используем эту функцию, чтобы заполнить базу данных товарами
async def add_items():
    await add_item(user_name="ASUS", user_tg_id=123, user_weight=123)
    await add_item(user_name="AS1US", user_tg_id=1123, user_weight=1123)


loop = asyncio.get_event_loop()
loop.run_until_complete(create_db())
loop.run_until_complete(add_items())