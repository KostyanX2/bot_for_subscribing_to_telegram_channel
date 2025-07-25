
from aiogram.types import Message
from aiogram import Router
from aiogram.filters import Command
from bot.buttons.payment import choice_pay
router = Router()

@router.message(Command(commands=['start']))
async def start(message: Message):
    text = 'ПРИВКИ!!!\nВЫБЕРИ ПОДПИСКУ'
    await message.answer(text=text, reply_markup=choice_pay())
