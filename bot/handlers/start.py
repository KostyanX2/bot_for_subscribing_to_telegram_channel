import os
from aiogram.enums import ChatMemberStatus
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import Router
from aiogram.filters import Command

from bot.buttons.extend_payments import extend_choice_pay
from bot.buttons.payment import choice_pay


router = Router()


@router.message(Command(commands=['start']))
async def start(message: Message, bot):
    user_channel_status = await bot.get_chat_member(os.getenv("CHANNEL_ID"), message.from_user.id)

    if user_channel_status.status not in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR]:
        markup = choice_pay()
        sent_msg = await message.answer("Выберите подписку:", reply_markup=markup)

    else:
        await message.answer("У вас уже есть активная подписка", reply_markup=extend_choice_pay())
