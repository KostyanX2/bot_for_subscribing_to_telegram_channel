import os

from aiogram.enums import ChatMemberStatus
from aiogram.types import Message
from aiogram import Router
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
from bot.buttons.payment import choice_pay
from bot.database.orm_query import check_time

router = Router()

@router.message(Command(commands=['start']))
async def start(message: Message,session: AsyncSession, bot):

    user_channel_status = await bot.get_chat_member(os.getenv("CHANNEL_ID"), message.from_user.id)
    if user_channel_status.status not in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR]:
        text = 'ПРИВКИ!!!\nВЫБЕРИ ПОДПИСКУ'
        markup = choice_pay()
    else:
        text = 'у вас уже есть активная подписка'
        markup = None

    await message.answer(text=text, reply_markup=markup)
