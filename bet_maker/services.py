from decimal import Decimal
import time

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import AsyncSessionLocal
from models import Bet, User
from schemas.external import Event
from schemas.incoming import Bet as BetModel


async def get_db():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()


async def get_user_in_db(username: str, db: AsyncSession) -> User | None:
    stmt = select(User).where(User.name == username)
    rows = await db.execute(stmt)
    return rows.first()


async def get_user_by_id(user_id: int, db: AsyncSession) -> User | None:
    stmt = select(User).where(User.id == user_id)
    rows = await db.execute(stmt)
    return rows.first()


async def create_user(username: str, db: AsyncSession) -> User | None:
    if await get_user_in_db(username, db) is None:
        user = User(name=username)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
    return None


async def get_event_by_id(event_id: int) -> Event:
    return Event(
        id=event_id,
        coefficient=Decimal('1.23'),
        state="open",
        deadline=time.time(),
    )

async def create_bet(
        user: User,
        bet: BetModel,
        db: AsyncSession
) -> Bet | None:
    if bet.bid > user.balance:
        return None
    user.balance -= bet.bid
    # noinspection PyTypeChecker
    new_bet = Bet(user_id=user.id, **bet.model_dump())
    db.add(new_bet)
    await db.commit()
    await db.refresh(new_bet)
    return new_bet


async def get_user_bets(user: User, db: AsyncSession) -> list[Bet]:
    stmt = select(Bet).where(Bet.user_id == user.id)
    rows = await db.execute(stmt)
    # noinspection PyTypeChecker
    return rows.all()
