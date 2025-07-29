import os

from aiogram import Bot, Dispatcher
import asyncio
import os

from bot.check_subscriptions import check_subscriptions
from bot.handlers import payment, start, accident
from bot.database.engine import create_database, drop_database, session_maker
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bot.middlewares.database import DataBaseSession

load_dotenv()

bot = Bot(os.getenv("TOKEN"))
dp = Dispatcher()
scheduler = AsyncIOScheduler()

async def on_startup(bot):
    run_param = False
    if run_param:
        await drop_database()
    await create_database()


async def on_shutdown(bot):
    print("Shutting down... БОТ ЛЁГ")


async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.include_routers(payment.router, start.router, accident.router )
    dp.update.middleware(DataBaseSession(session_pool=session_maker))
    await create_database()
    scheduler.add_job(
        check_subscriptions,
        "interval",
        hours=12,
        args=(bot,)
    )
    scheduler.start()

    try:
        await dp.start_polling(bot)
    finally:
        scheduler.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
