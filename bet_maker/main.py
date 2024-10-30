import asyncio
from contextlib import asynccontextmanager
from uuid import uuid4

from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import PositiveInt
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import incoming as inc, outgoing as out, external as ext
from services import (
    create_user, get_db, get_user_by_id, create_bet, get_user_bets,
    wait_for_events, get_available_events
)
from settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(wait_for_events())
    yield


app = FastAPI(**settings.app, lifespan=lifespan)


@app.get("/events", tags=["Event"])
@handle_exception
async def get_events(db: AsyncSession = Depends(get_db)) -> ext.NewEvents:
    """Возвращает из БД события на которые ещё можно сделать ставку. """
    events = [
        ext.Event.model_validate(e[0]) for e in await get_available_events(db)
    ]
    return ext.NewEvents(events=events)


@app.post("/bet", status_code=status.HTTP_201_CREATED, tags=["Bet"])
async def add_bet(bet: inc.Bet, db: AsyncSession = Depends(get_db)) -> out.Bet:
    """ Делает ставку на событие, подразумевается возможность сделать
     идентичную ставку повторно.
    """
    # Да, на текущий момент притягиваем всё к одному пользователю
    _temp_user_id = 1
    if user := await get_user_by_id(1, db):
        # noinspection PyUnresolvedReferences
        if bet_ := await create_bet(user[0], bet, db):
            return out.Bet.model_validate(bet_)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Either Event {bet.event_id} Do Not Exists Or Not Enough "
                   f"Money"
        )
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized"
    )


@app.get("/bets", tags=["Bet"])
async def get_bets(db: AsyncSession = Depends(get_db)) -> out.UserBets:
    """Возвращает все ставки сделанные конкретным юзером. """
    _temp_user_id = 1
    if user := await get_user_by_id(1, db):
        return out.UserBets(bets=await get_user_bets(user[0], db))
    raise HTTPException(status_code=401, detail="Unauthorized")


@app.post("/user", status_code=status.HTTP_201_CREATED, tags=["User"])
async def add_user(db: AsyncSession = Depends(get_db)) -> out.User:
    """ Добавляет пользователя в БД, пока что для простоты генерируем юзернейм
     прям тут
    """
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
    """Вернуть данные о пользователе через id """
    if user := await get_user_by_id(user_id, db):
        r_user = out.User.model_validate(user[0])
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
