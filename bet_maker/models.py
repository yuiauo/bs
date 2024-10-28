from __future__ import annotations
from decimal import Decimal
import time
from typing import Literal

from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs


EventState = Literal["open", "win1", "win2"]


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    """Таблица с пользователями """
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True)
    balance: Mapped[Decimal] = mapped_column(Numeric(scale=2), default=0)
    bets: Mapped[list[Bet]] = relationship(cascade="all, delete")


class Bet(Base):
    """Таблица ставок """
    __tablename__ = "bets"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    bid: Mapped[Decimal] = mapped_column(Numeric(precision=6, scale=2))
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))


class Event(Base):
    """Таблица событий. Не уверен, что их нужно было хранить, но допустим. """
    __tablename__ = "events"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    coefficient: Mapped[Decimal] = mapped_column(Numeric(precision=3, scale=2))
    state: Mapped[EventState]
    deadline: Mapped[int] = mapped_column(default=time.time())
    description: Mapped[str | None]
