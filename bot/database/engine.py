import os
from dotenv import load_dotenv
load_dotenv()
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from bot.database.models import Base

engine = create_async_engine(os.getenv('DATABASE_URL'), echo=True, future=True)

session_maker = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def create_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def drop_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)