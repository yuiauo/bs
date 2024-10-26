from decimal import Decimal

from pydantic import BaseModel, Field, PositiveInt

from . import EventState

class Event(BaseModel):
    """Event model """
    id: PositiveInt
    coefficient: Decimal = Field(gt=0)
    state: EventState
    deadline: PositiveInt
    description: str | None = None
