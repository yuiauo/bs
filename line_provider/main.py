import time

from aio_pika.abc import AbstractChannel
from fastapi import Depends, FastAPI, HTTPException, status
from starlette.responses import RedirectResponse

from schemas import EventCreated
from lp_typing import EventType
from schemas import Event, EventList
from services import EventStorage, get_channel, get_db, send_events
from settings import APISettings


app = FastAPI(**APISettings().model_dump())


@app.post("/event", status_code=status.HTTP_201_CREATED, tags=["Event"])
async def create_event(
        event: Event,
        channel: AbstractChannel = Depends(get_channel),
        db: EventStorage = Depends(get_db)
) -> EventCreated:
    if event.deadline > time.time() and event.state != "open":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=""
        )
    if event in db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Event already exists"
        )
    await db.add(event)
    await send_events(channel, db)
    return EventCreated(event_id=event.id)


@app.get("/event/{event_id}", tags=["Event"])
async def get_event(
        event_id: int, db: EventStorage = Depends(get_db)
) -> Event:
    if event := await db.get(event_id):
        return event
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event not found"
    )


@app.get("/events/{event_type}", response_model=None, tags=["Event"])
async def get_events(
        event_type: EventType,
        db: EventStorage = Depends(get_db)
) -> EventList | RedirectResponse:
    if event_type == "all":
        return RedirectResponse(url='/events')
    # cast(EventState, event_type)
    return db[event_type]


@app.get("/events", tags=["Event"])
async def get_events(db: EventStorage = Depends(get_db)) -> EventList:
    return EventList(events=db.all)
