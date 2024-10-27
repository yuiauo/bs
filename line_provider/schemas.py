from decimal import Decimal
import json

from pydantic import BaseModel, Field, PositiveInt

from lp_typing import EventState


class Event(BaseModel):
    """ Модель события """
    id: PositiveInt
    coefficient: Decimal = Field(gt=1)
    state: EventState
    deadline: PositiveInt = Field(ge=15e8, le=20e8)
    description: str | None = None

    def to_bytes(self) -> bytes:
        python_dict = self.model_dump()
        return json.dumps(python_dict).encode()


class EventCreated(BaseModel):
    event_id: PositiveInt = Field(ge=1)


class EventList(BaseModel):
    events: list[Event]
