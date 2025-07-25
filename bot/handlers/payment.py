import os
import time
from main import bot
from aiogram import Router, types, F, Bot
from aiogram.types import Message,  PreCheckoutQuery, CallbackQuery
from dotenv import load_dotenv
load_dotenv()

bot = bot
router = Router()

async def generate_link(message: Message):
    link = await bot.create_chat_invite_link(chat_id=os.getenv("CHANNEL_ID"),name=str(message.chat.id), member_limit=1, expire_date=int(time.time()) + 86400)
    return link.invite_link


@router.callback_query(F.data == 'month')
async def month_payment(call: CallbackQuery):
    await bot.send_invoice(call.message.chat.id, 'Подписка на месяц', 'подписка на тгк', 'month_sub', provider_token=os.getenv("PAY_TOKEN"), currency="rub", prices=[types.LabeledPrice(label="Месяц", amount=10000)])

@router.callback_query(F.data == 'year')
async def year_payment(call: CallbackQuery):
    await bot.send_invoice(call.message.chat.id, 'Подписка на год', 'подписка на тгк', 'year_sub', provider_token=os.getenv("PAY_TOKEN"), currency="rub", prices=[types.LabeledPrice(label="Год", amount=100000)])

@router.pre_checkout_query()
async def pre_checkout(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(
        pre_checkout_query_id=pre_checkout_query.id,
        ok=True,
        error_message=None
    )


@router.message(F.content_type == 'successful_payment')
async def successful_payment(message: Message):
    payment = message.successful_payment
    amount = payment.total_amount / 100
    invite_link = await generate_link(message)
    await message.answer(
        f"✅ Платеж на сумму {amount} руб. успешно проведен!\n"
        f"Ваша ссылка для доступа: {invite_link}"
    )
    print(payment)
    if payment.invoice_payload == 'month':
        print('ORM')
    else:
        print('ORM YEAR')




