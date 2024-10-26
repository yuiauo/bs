from decimal import Decimal
from pydantic import BaseModel, Field, PositiveInt

from lp_typing import EventState


class Event(BaseModel):
    """ Модель события """
    id: PositiveInt
    coefficient: Decimal = Field(gt=0)
    state: EventState
    deadline: PositiveInt
    description: str | None = None
