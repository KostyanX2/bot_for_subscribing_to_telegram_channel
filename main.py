import os

from aiogram import Bot, Dispatcher
import asyncio
import os
from bot.handlers import payment, start
from bot.database.engine import create_database, drop_database
from dotenv import load_dotenv
load_dotenv()

bot = Bot(os.getenv("TOKEN"))
dp = Dispatcher()


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
    dp.include_routers(payment.router, start.router )

    await dp.start_polling(bot)
    await create_database()



if __name__ == "__main__":
    asyncio.run(main())