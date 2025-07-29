import os
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta, timezone
from aiogram.fsm.state import StatesGroup, State
from bot.database.orm_query import orm_add_user, check_user, orm_update_user
from aiogram import Router, types, F
from aiogram.types import Message, PreCheckoutQuery, CallbackQuery
from dotenv import load_dotenv

load_dotenv()



router = Router()


async def generate_link(message: Message, bot):
    link = await bot.create_chat_invite_link(
        chat_id=int(os.getenv("CHANNEL_ID")),
        name=str(message.chat.id),
        member_limit=1,
        expire_date=datetime.now(timezone.utc) + timedelta(days=1)
    )
    return link.invite_link



@router.callback_query(F.data == 'month')
async def month_payment(call: CallbackQuery):

    await call.message.edit_text(
        text="Вы выбрали подписку на месяц",
        reply_markup=InlineKeyboardBuilder().as_markup()
    )

    await call.message.answer_invoice(
        title='Подписка на месяц',
        description='подписка на тгк',
        payload='month_sub',
        provider_token=os.getenv("PAY_TOKEN"),
        currency="rub",
        prices=[types.LabeledPrice(label="Месяц", amount=10000)]
    )
@router.callback_query(F.data == 'year')
async def year_payment(call: CallbackQuery):

    await call.message.edit_text(
        text="Вы выбрали подписку на год",
        reply_markup=InlineKeyboardBuilder().as_markup()
    )

    await call.message.answer_invoice(
        title='Подписка на год',
        description='подписка на тгк',
        payload='year_sub',
        provider_token=os.getenv("PAY_TOKEN"),
        currency="rub",
        prices=[types.LabeledPrice(label="Год", amount=100000)]
    )

@router.pre_checkout_query()
async def pre_checkout(pre_checkout_query: PreCheckoutQuery, bot):
    await bot.answer_pre_checkout_query(
        pre_checkout_query_id=pre_checkout_query.id,
        ok=True,
        error_message=None
    )


@router.message(F.content_type == 'successful_payment')
async def successful_payment(message: Message, session: AsyncSession, bot):
    payment = message.successful_payment
    amount = payment.total_amount // 100
    time =  datetime.now() + timedelta(days=30) if payment.invoice_payload == 'month_sub' else datetime.now() + timedelta(days=365)
    user_data = {
        'id': message.from_user.id,
        'username': message.from_user.username,
        'user_id': message.from_user.id,
        'payment': True,
        'time': time
    }
    if await check_user(session, user_data['user_id']):
        time = time + timedelta(
            days=30) if payment.invoice_payload == 'month_sub' else time + timedelta(days=365)
        user_data['time'] = time
        await orm_update_user(session, user_data)
        period = 'Месяц' if payment.invoice_payload == 'month_sub' else 'год'
        await message.answer(f"✅ Платеж на сумму {amount} руб. успешно проведен!\nПодписка на {period}")
    else:
        invite_link = await generate_link(message, bot)
        await message.answer(
            f"✅ Платеж на сумму {amount} руб. успешно проведен!\n"
            f"Ваша ссылка для доступа: {invite_link}"
        )
        await orm_add_user(session, user_data)





