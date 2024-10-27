import time
from uuid import uuid4

from fastapi import Depends, FastAPI, HTTPException, Path, status
from pydantic import PositiveInt
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import incoming as inc, outgoing as out, external as ext
from services import (
    create_user, get_db, get_user_by_id, create_bet, get_user_bets
)
from settings import settings


app = FastAPI(**settings.api)


@app.get("/events", tags=["Event"])
async def get_events() -> list[ext.Event]:
    ...
    return []


@app.get("/event", tags=["Event"])
async def get_event_by_id() -> ext.Event:
    ...
    return ext.Event()


@app.post("/bet", status_code=status.HTTP_201_CREATED, tags=["Bet"])
async def add_bet(bet: inc.Bet, db: AsyncSession = Depends(get_db)) -> out.Bet:
    """ Подразумевается возможность сделать идентичную ставку повторно. """
    _temp_user_id = 1
    if user := await get_user_by_id(1, db):
        if bet := await create_bet(user[0], bet, db):
            return out.Bet.model_validate(bet)
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="Payment Failed"
        )
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized"
    )


@app.get("/bets", tags=["Bet"])
async def get_bets(db: AsyncSession = Depends(get_db)) -> out.UserBets:
    _temp_user_id = 1
    if user := await get_user_by_id(1, db):
        bets = await get_user_bets(user[0], db)
        return out.UserBets.model_validate(bets)
    raise HTTPException(status_code=401, detail="Unauthorized")

@app.post("/user", status_code=status.HTTP_201_CREATED, tags=["User"])
async def add_user(db: AsyncSession = Depends(get_db)) -> out.User:
    # пока что для простоты генерируем юзернейм прям тут
    new_username = str(uuid4())
    if user := await create_user(new_username, db):
        r_user = out.User.model_validate(user)
        return r_user
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="User Already Exists"
    )


@app.get("/user/{user_id}", tags=["User"])
async def get_user(
    user_id: PositiveInt,
    db: AsyncSession = Depends(get_db)
) -> out.User:
    if user := await get_user_by_id(user_id, db):
        r_user = out.User.model_validate(user)
        return r_user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User Not Found"
    )


@app.get("/users", tags=["User"])
async def get_users(db: AsyncSession = Depends(get_db)) -> out.User:
    """ Возвращает всех пользователей """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Not Implemented"
    )
