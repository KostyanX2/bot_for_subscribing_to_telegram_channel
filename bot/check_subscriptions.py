import os
from datetime import datetime

from aiogram.enums import ChatMemberStatus
from dotenv import load_dotenv

from bot.buttons.extend_payments import extend_choice_pay
from bot.database.engine import session_maker

from bot.database.orm_query import check_time, orm_delete_user

load_dotenv()



async def check_subscriptions(bot):
    async with session_maker() as session:
        data = await check_time(session)
        now = datetime.now()
        for user in data:
            chat_member = await bot.get_chat_member(os.getenv("CHANNEL_ID"), user.user_id)
            days_left = (user.time - now).days
            if days_left <= 7:
                await bot.send_message(chat_id=user.user_id, text=f"У вас осталось {days_left} активных дней подписки, продлить:", reply_markup=extend_choice_pay())
            if days_left <= 0 and chat_member.status != ChatMemberStatus.ADMINISTRATOR and chat_member.status != ChatMemberStatus.CREATOR:
                await bot.ban_chat_member(
                    chat_id=os.getenv("CHANNEL_ID"),
                    user_id=user.user_id
                )
                await bot.unban_chat_member(
                    chat_id=os.getenv("CHANNEL_ID"),
                    user_id=user.user_id
                )
                await orm_delete_user(session, user.user_id)









