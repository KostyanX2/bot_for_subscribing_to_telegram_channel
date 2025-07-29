from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from bot.database.models import Users

async def orm_add_user(session: AsyncSession, data: dict) -> None:
    user = Users(
        id = data['id'],
        username=data['username'],
        user_id=data['user_id'],
        payment=data['payment'],
        time=data['time']
    )
    session.add(user)
    await session.commit()


async def orm_delete_user(session: AsyncSession, user_id: int):
    query = delete(Users).where(Users.id == user_id)
    await session.execute(query)
    await session.commit()


async def orm_update_user(session: AsyncSession, data: dict) -> None:
    query = update(Users).where(Users.id == data['user_id']).values(time=data['time'])
    await session.execute(query)
    await session.commit()

async def check_time(session: AsyncSession):
    query = select(Users)
    result = await session.execute(query)
    return result.scalars().all()



async def check_user(session: AsyncSession, user_id: int):
    query = select(Users).where(Users.id == user_id)
    result = await session.execute(query)
    return result.scalar_one_or_none() is not None