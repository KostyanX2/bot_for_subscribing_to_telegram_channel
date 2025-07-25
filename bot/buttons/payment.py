from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def choice_pay():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Подписка на месяц. 100 руб.', callback_data='month')],
            [InlineKeyboardButton(text='Подписка на год. 1000 руб.', callback_data='year')]
        ]
    )