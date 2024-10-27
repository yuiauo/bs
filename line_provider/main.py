from contextlib import asynccontextmanager
import time

from fastapi import Depends, FastAPI, Path, HTTPException

from database import EventStorage, storage
from schemas import Event
from services import get_channel, send_event


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     connection = await anext(get_db())
#     channel = await connection.channel()
#     await channel.declare_queue(EVENT_QUEUE, durable=True)
#     yield
#     await channel.close()
#     await connection.close()


app = FastAPI()


@app.post('/event', status_code=201)
async def create_event(
        event: Event, db: EventStorage = Depends(storage)
) -> int:
    if event in db:
        raise HTTPException(status_code=409, detail='Event already exists')
    await db.add(event)
    return event


# @app.get('/event/{event_id}')
# async def get_event(event_id: int = Path(default=None)):
#     if event_id in events:
#         return events[event_id]
#
#     raise HTTPException(status_code=404, detail="Event not found")


# @app.get('/events')
# async def get_events():
#     return list(e for e in events.values() if time.time() < e.deadline)
