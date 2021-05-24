from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


average_weight_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('Средний вес за 7 дней', callback_data='average7'),
    InlineKeyboardButton('Средний вес за 28 дней', callback_data='average28')]
])

