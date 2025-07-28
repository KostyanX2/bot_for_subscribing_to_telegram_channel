from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def extend_choice_pay():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Продлить подписку на месяц. 100 руб.', callback_data='month')],
            [InlineKeyboardButton(text='Продлить подписку на год. 1000 руб.', callback_data='year')]
        ]
    )
