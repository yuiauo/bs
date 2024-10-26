from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import AsyncSession as AsyncSessionLocal
from models import User
from schemas.outgoing import User as UserModel


async def get_db():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()


async def check_user_in_db(username: str, db: AsyncSession) -> User | None:
    stmt = select(User).where(User.name == username)
    rows = await db.execute(stmt)
    return rows.first()


async def check_user_by_id(user_id: str, db: AsyncSession) -> User | None:
    stmt = select(User).where(User.id == user_id)
    rows = await db.execute(stmt)
    return rows.first()


async def create_user(username: str, db: AsyncSession) -> User | None:
    if await check_user_in_db(username, db) is None:
        user = User(name=username)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
    return None