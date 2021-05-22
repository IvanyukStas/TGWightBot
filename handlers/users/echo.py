from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from utils.db_api.db_commands import create_user_weight, update_user_weight


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния



@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    if not message.text.isdigit():
        await message.answer(f"Чертило не тупи, напиши свой вес цифрами!!!!!")
        await message.answer(f"Эхо без состояния."
                             f"Сообщение:\n"
                             f"{message.text}")
    else:
        print('inache')
        await update_user_weight(message.from_user.id, message.text)
        await message.answer(f'Мы хаписали ваш вес - {message.text}\n'
                             f'Чтобы узнать средний вес за 7 дней на;мите /7\n'
                             f'За 28 дней /28')
    #await create_user_weight(user_weight=message.text, user_tg_id=message.from_user.id)


# Эхо хендлер, куда летят ВСЕ сообщения с указанным состоянием
@dp.message_handler(state="*", content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    state = await state.get_state()
    await message.answer(f"Эхо в состоянии <code>{state}</code>.\n"
                         f"\nСодержание сообщения:\n"
                         f"<code>{message}</code>")
