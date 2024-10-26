import time
from uuid import uuid4

from fastapi import Depends, FastAPI, HTTPException, Path
from pydantic import PositiveInt
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import incoming as inc, outgoing as out, external as ext
from services import (
    create_user, get_db, get_user_by_id, create_bet, get_user_bets
)
from settings import settings


app = FastAPI(**settings.app)


@app.get("/events")
async def get_events() -> list[ext.Event]:
    ...
    return []


@app.get("/event")
async def get_event_by_id() -> ext.Event:
    ...
    return ext.Event()


@app.post("/bet")
async def add_bet(bet: inc.Bet, db: AsyncSession = Depends(get_db)) -> out.Bet:
    """ Подразумевается возможность сделать идентичную ставку повторно. """
    _temp_user_id = 1
    if user := await get_user_by_id(1, db):
        if bet := await create_bet(user, bet, db):
            return out.Bet.model_validate(bet)
        raise HTTPException(status_code=402, detail="Payment Failed")
    raise HTTPException(status_code=401, detail="Unauthorized")


@app.get("/bets")
async def get_bets(user_id: PositiveInt, db: AsyncSession) -> out.UserBets:
    _temp_user_id = 1
    if user := await get_user_by_id(1, db):
        bets = await get_user_bets(user, db)
        return out.UserBets.model_validate(bets)
    raise HTTPException(status_code=401, detail="Unauthorized")

@app.post("/user")
async def add_user(db: AsyncSession = Depends(get_db)) -> out.User:
    # пока что для простоты генерируем юзернейм прям тут
    new_username = str(uuid4())
    if user := await create_user(new_username, db):
        r_user = out.User.model_validate(user)
        return r_user
    raise HTTPException(status_code=409, detail="User Already Exists")


@app.get("/user/{user_id}")
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
) -> out.User:
    if user := await get_user_by_id(user_id, db):
        r_user = out.User.model_validate(user)
        return r_user
    raise HTTPException(status_code=404, detail="User Not Found")


@app.get("/users")
async def get_users(db: AsyncSession = Depends(get_db)) -> out.User:
    """ Возвращает всех пользователей """
    raise HTTPException(status_code=501, detail="Not Implemented")
