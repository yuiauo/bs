from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, Field, PlainSerializer, PositiveInt


class OutgoingModel(BaseModel, from_attributes=True):
    pass


class Login(OutgoingModel):
    username: str
    password: str
    user_id: int


class User(OutgoingModel):
    id: PositiveInt
    balance: Decimal = Field(ge=Decimal("0.0"), decimal_places=2)
    name: str


class Bet(OutgoingModel):
    """Bet model to be returned """
    id: PositiveInt | None = None
    bid: Decimal = Field(gt=0, lt=1e4)
    event_id: PositiveInt
    user_id: PositiveInt


class UserBets(OutgoingModel):
    bets: list[Bet]
