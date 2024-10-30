from decimal import Decimal
import json
from typing import AsyncGenerator

import aio_pika
from aio_pika.abc import AbstractChannel, AbstractQueue
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import AsyncSessionLocal
from logger import logger
from models import Bet, Event, User
from schemas.external import Event as EventModel
from schemas.incoming import Bet as BetModel
from settings import settings
from utils import handle_exception



async def get_channel() -> AsyncGenerator[AbstractChannel, None]:
    connection = await aio_pika.connect(settings.env.RABBITMQ_URL)
    channel = await connection.channel()
    await channel.declare_queue(settings.env.EVENT_QUEUE, durable=True)
    try:
        yield channel
    finally:
        await connection.close()


async def wait_for_events():
    connection = await aio_pika.connect(settings.env.RABBITMQ_URL)
    channel = await connection.channel()
    await process_events(channel)
    await channel.close()
    await connection.close()


async def process_events(channel: AbstractChannel) -> None:
    queue = await channel.declare_queue(
        settings.env.EVENT_QUEUE, durable=True
    )
    async for new_event in new_events(queue):

        async with AsyncSessionLocal() as db:
            if event := await get_event(new_event.id, db):
                logger.info("New rabbit message received. "
                            "Updating local copy of it...")
                await _update_event(event[0], new_event, db)
            else:
                logger.info("New rabbit message received. "
                            "Creating local copy of it...")
                await add_event(new_event, db)


async def new_events(queue: AbstractQueue) -> AsyncGenerator[Event, None]:
    async with queue.iterator() as qi:
        async for message in qi:
            async with message.process():
                incoming_json = json.loads(message.body)
                event = EventModel.model_validate_json(incoming_json)
                # предположительно тут происходит RPC таймаут
                yield event


async def get_db():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()


@handle_exception
async def get_user_in_db(username: str, db: AsyncSession) -> User | None:
    stmt = select(User).where(User.name == username)
    rows = await db.execute(stmt)
    logger.info(f"Returning user with {username=}")
    return rows.first()


@handle_exception
async def get_user_by_id(user_id: int, db: AsyncSession) -> User | None:
    stmt = select(User).where(User.id == user_id)
    rows = await db.execute(stmt)
    logger.info(f"Returning user with {user_id=}")
    return rows.first()


@handle_exception
async def create_user(username: str, db: AsyncSession) -> User | None:
    if await get_user_in_db(username, db) is None:
        user = User(name=username, balance=Decimal(100))
        db.add(user)
        await db.commit()
        await db.refresh(user)
        logger.info(f"Returning user with {username=}")
        return user
    return None


@handle_exception
async def get_event(event_id: int, db: AsyncSession) -> Event:
    stmt = select(Event).where(Event.id == event_id)
    rows = await db.execute(stmt)
    logger.info(f"Returning event with {event_id=}")
    # noinspection PyTypeChecker
    return rows.first()


@handle_exception
async def get_available_events(db: AsyncSession):
    """Возвращает все доступные для ставки события. """
    stmt = select(Event).where(Event.state == "open")
    rows = await db.execute(stmt)
    logger.info(f"Returning all available events")
    return rows.all()


@handle_exception
async def add_event(event_schema: EventModel, db: AsyncSession) -> Event:
    event = Event(**event_schema.model_dump())
    db.add(event)
    await db.commit()
    await db.refresh(event)
    logger.info(f"Event with {event.id=} created.")
    return event


@handle_exception
async def _update_event(
    event: Event, new_event_schema: EventModel, db: AsyncSession
) -> None:
    """У обновляемого события может измениться только статус или
     коэффициент.
    """
    event.coefficient = new_event_schema.coefficient
    event.state = new_event_schema.state
    event.description = new_event_schema.description
    await db.commit()
    logger.info(f"Event with {event.id=} updated.")


@handle_exception
async def create_bet(
    user: User,
    bet: BetModel,
    db: AsyncSession
) -> Bet | None:
    if await get_event(bet.event_id, db) is not None:
        if bet.bid > user.balance:
            # это пока никак не обрабатывается
            logger.info(f"Not enough money. Current balance: {user.balance}")
            return None
        user.balance -= bet.bid
        # noinspection PyTypeChecker
        new_bet = Bet(user_id=user.id, **bet.model_dump())
        db.add(new_bet)
        await db.commit()
        await db.refresh(user)
        logger.info(f"Bet successful. Current balance: {user.balance}")
        return new_bet
    return None


@handle_exception
async def get_user_bets(user: User, db: AsyncSession):
    stmt = select(Bet).where(Bet.user_id == user.id)
    rows = await db.execute(stmt)
    # noinspection PyTypeChecker
    logger.info(f"Returning all user bets")
    return rows.all()
