from decimal import Decimal
import json
import time
from typing_extensions import Self

from pydantic import BaseModel, Field, model_validator, PositiveInt

from lp_typing import EventState


class Event(BaseModel):
    """Схема валидации входящего события. Допустимо добавлять события до
    мая 2033 года (2 млрд таймстамп) """
    id: PositiveInt
    coefficient: Decimal = Field(gt=1)
    state: EventState
    deadline: PositiveInt = Field(ge=15e8, le=2e9)
    description: str | None = None

    def to_bytes(self) -> bytes:
        python_dict = self.model_dump_json()
        return json.dumps(python_dict).encode()

    @model_validator(mode="after")
    def check_if_expired(self) -> Self:
        """Проверяет валидность времени/статуса """
        if self.deadline <= time.time():
            if self.state == "open":
                raise ValueError("Can't be `open` after deadline")
        else:
            if self.state != "open":
                raise ValueError("Can't find winner before deadline")
        return self


class UpdateEvent(BaseModel):
    """Схема валидации события для patch. На текущий момент можно менять
     только коэффициент и описание """
    coefficient: Decimal | None = Field(gt=1, default=None)
    description: str | None = None

# ================ Возвращаемые схемы событий ===============

class EventCreated(BaseModel):
    event_id: PositiveInt = Field(ge=1)


class EventList(BaseModel):
    events: list[Event]
