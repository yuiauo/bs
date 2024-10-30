from aio_pika.abc import AbstractChannel
from fastapi import Depends, FastAPI, HTTPException, status
from starlette.responses import RedirectResponse

from schemas import EventCreated, UpdateEvent
from lp_typing import EventType
from schemas import Event, EventList
from services import EventStorage, get_channel, get_db, send_events
from settings import settings


app = FastAPI(**settings.app)


@app.post("/event", status_code=status.HTTP_201_CREATED, tags=["Event"])
async def create_event(
        event: Event,
        channel: AbstractChannel = Depends(get_channel),
        db: EventStorage = Depends(get_db)
) -> EventCreated:
    """Создания события """
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
    """Возвращает событие под определенным id"""
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
    """Возвращает определенную категорию хранящихся событий.
    Категории: 'open', 'all', 'win1', 'win2'
    """
    if event_type == "all":
        return RedirectResponse(url='/events')
    # cast(EventState, event_type)
    return db[event_type]


@app.get("/events", tags=["Event"])
async def get_events(db: EventStorage = Depends(get_db)) -> EventList:
    """Все хранящиеся события в псевдобазе """
    return EventList(events=db.all)


@app.patch("/event/{event_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_event(
    event_id: int,
    updates: UpdateEvent,
    channel: AbstractChannel = Depends(get_channel),
    db: EventStorage = Depends(get_db)
) -> Event:
    """Обновляет событие"""
    if event := await db.get(event_id):
        event.coefficient = updates.coefficient
        event.description = updates.description
        await db.update(event)
        await send_events(channel, db)
        return event
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Event {event_id} Not Found"
    )
