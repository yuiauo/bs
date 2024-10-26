from decimal import Decimal

from pydantic import BaseModel, Field, PositiveInt, PositiveFloat

from . import EventState

class Event(BaseModel):
    """Event model """
    id: PositiveInt
    # нет смысла ставить, если коэффициент <= 1
    coefficient: Decimal = Field(gt=1)
    state: EventState
    deadline: PositiveFloat
    description: str | None = None
