import time

from fastapi import FastAPI, Path, HTTPException
from fastapi.responses import JSONResponse
from schemas import Event


events: dict[int, Event] = {}

app = FastAPI()


@app.post('/event')
async def create_event(event: Event):
    if event.event_id not in events:
        events[event.event_id] = event
        return JSONResponse(status_code=201, content=event.model_dump(by_alias=True))

    else:
        raise HTTPException(status_code=409, detail='Event already exists')
    # for p_name, p_value in event.dict(exclude_unset=True).items():
    #     setattr(events[event.event_id], p_name, p_value)
    #
    # return {}


@app.get('/event/{event_id}')
async def get_event(event_id: int = Path(default=None)):
    if event_id in events:
        return events[event_id]

    raise HTTPException(status_code=404, detail="Event not found")


@app.get('/events')
async def get_events():
    return list(e for e in events.values() if time.time() < e.deadline)
