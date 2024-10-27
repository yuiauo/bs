from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, Field, PlainSerializer, PositiveInt


class Login(BaseModel):
    username: str
    password: str


class Bet(BaseModel):
    """Input Bet model """
    bid: Decimal = Field(gt=Decimal("0.0"), lt=1e4, decimal_places=2)
    event_id: PositiveInt

