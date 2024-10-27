from decimal import Decimal
import json
from typing import Literal

from pydantic import BaseModel, Field, PositiveInt


EventState = Literal["open", "win1", "win2"]


class Event(BaseModel):
    """ Модель события """
    id: PositiveInt
    coefficient: Decimal = Field(gt=0)
    state: EventState
    deadline: PositiveInt
    description: str | None = None

    def to_bytes(self) -> bytes:
        python_dict = self.model_dump()
        return json.dumps(python_dict).encode()
