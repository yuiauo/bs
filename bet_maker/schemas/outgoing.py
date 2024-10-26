from decimal import Decimal

from pydantic import BaseModel, Field, PositiveInt


class OutgoingModel(BaseModel):

    class Config:
        from_attributes = True

class Login(OutgoingModel):
    username: str
    password: str

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

