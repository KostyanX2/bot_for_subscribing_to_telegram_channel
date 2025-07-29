import os
from aiogram import types
from aiogram import Router
from aiogram.enums import ChatMemberStatus
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
from bot.handlers.payment import generate_link
from bot.database.orm_query import check_user

router = Router()

@router.message(Command(commands=['accident']))
async def accident(message: types.Message, session: AsyncSession, bot):
    user_channel_status = await bot.get_chat_member(os.getenv("CHANNEL_ID"), message.from_user.id)
    if await check_user(session, message.from_user.id) and user_channel_status.status in [ChatMemberStatus.LEFT]:
        link = await generate_link(message, bot)
        await message.answer(f'Ваша ссылка для потворного входа: {link}\nНе теряйтесь!')
    else:
        await message.answer(f'Вы подписаны на канал')