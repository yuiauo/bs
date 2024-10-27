from __future__ import annotations
from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs


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
    event_id: Mapped[int]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
