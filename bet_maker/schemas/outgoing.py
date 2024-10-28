"""Схемы используемые в качестве ответа апи"""

from decimal import Decimal

from pydantic import BaseModel, Field, PositiveInt


class OutgoingModel(BaseModel, from_attributes=True):
    """ Условно абстрактный класс для подгрузки с БД """
    pass


class Login(OutgoingModel):
    """Успешный логин вернёт user_id по которому можно стянуть юзера """
    username: str
    user_id: int


class User(OutgoingModel):
    """ """
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
