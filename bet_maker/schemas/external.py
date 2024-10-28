from decimal import Decimal

from pydantic import BaseModel, Field, PositiveInt, PositiveFloat

from . import EventState


class Event(BaseModel, from_attributes=True):
    """Схема события приходящего из сервиса line_provider.
    Локально используется для валидации перед добавлением в БД
    """
    id: PositiveInt
    # нет смысла ставить, если коэффициент <= 1
    coefficient: Decimal = Field(gt=1)
    state: EventState
    deadline: PositiveFloat
    description: str | None = None


class NewEvents(BaseModel):
    """Список событий, простоя схема для ответа апи """
    events: list[Event]
