import time

from fastapi import Depends, FastAPI, HTTPException, Path
from fastapi.responses import JSONResponse
from pydantic import PositiveInt
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import incoming as inc, outgoing as out, external as ext
from services import create_user, get_db

app = FastAPI()


@app.get("/events")
async def get_events() -> list[ext.Event]:
    ...
    return []

@app.get("/event")
async def get_event_by_id() -> ext.Event:
    ...
    return ext.Event()

@app.post("/bet")
async def add_bet(bet: inc.Bet) -> out.Bet:
    """ Подразумевается возможность сделать идентичную ставку повторно. """
    event = await get_event_by_id(bet.event_id)
    return out.Bet()

@app.get("/bets/{user_id}")
async def get_bets(user_id: PositiveInt) -> list[out.Bet]:
    user = await ...(user_id)
    return user.bets


@app.post("/user")
async def add_user(
        username: str,
        db: AsyncSession = Depends(get_db)
) -> out.User:
    if user := await create_user(username, db):
        r_user = out.User.model_validate(user)
        return r_user
    raise HTTPException(status_code=409, detail="User already exists")
#
#
# @app.get('/events')
# async def get_events():
#     return list(e for e in events.values() if time.time() < e.deadline)
