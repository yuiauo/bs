from __future__ import annotations
import asyncio
from functools import lru_cache
import os
import random
import time
from typing import AsyncGenerator, NoReturn
from queue import Queue

import aio_pika
from aio_pika.abc import AbstractChannel
from dotenv import load_dotenv

from lp_typing import EventState
from schemas import Event


load_dotenv()
RABBITMQ_URL = os.getenv("RABBITMQ_URL")
EVENT_QUEUE = "events"


async def get_db() -> AsyncGenerator:
    db = EventStorage()
    yield db


async def get_channel() -> AsyncGenerator[AbstractChannel, None]:
    connection = await aio_pika.connect(RABBITMQ_URL)
    channel = await connection.channel()
    await channel.declare_queue(EVENT_QUEUE, durable=True)
    try:
        yield channel
    finally:
        await connection.close()


def compose_message(message: Event) -> aio_pika.Message:

    return aio_pika.Message(
        body=message.to_bytes(),
        content_type="application/json",
        content_encoding="utf-8",
        delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
    )


async def send_event(event: Event, channel: AbstractChannel) -> None:
    await channel.default_exchange.publish(
        compose_message(event), routing_key=EVENT_QUEUE
    )


async def send_events(channel: AbstractChannel, db: EventStorage) -> None:
    """Закидвает в раббит новые и обновленные события """
    tasks = [send_event(event, channel) for event in db.get_updates()]
    await asyncio.gather(*tasks)


@lru_cache
class EventStorage:
    """ Ввиду спешки решил хранить и обновлять события так """
    __DELAY: int = 5

    def __init__(self, delay: int | float = __DELAY):
        self.delay = delay
        self.completed_win1 = []
        self.completed_win2 = []
        self.pending = []
        self.fifo_changes = Queue()

    async def add(self, event: Event) -> None | NoReturn:
        match event.state:
            case "win1":
                self.completed_win1.append(event)
            case "win2":
                self.completed_win2.append(event)
            case "open":
                self.pending.append(event)
            case _:
                raise ValueError
        self.fifo_changes.put(event)

    async def update(self, event: Event) -> None | NoReturn:
        self.fifo_changes.put(event)

    def __getitem__(self, state: EventState) -> list[Event] | NoReturn:
        match state:
            case "win1":
                return self.completed_win1
            case "win2":
                return self.completed_win2
            case "open":
                return self.pending
            case _:
                raise ValueError(
                    "Only 'win1', 'win2' and 'open' options are available"
                )

    def __contains__(self, event: Event) -> bool:
        for inner_event in self.all:
            if event.id == inner_event.id:
                return True
        return False

    async def get(self, event_id: int) -> Event | None:
        for event in self.all:
            if event.id == event_id:
                return event

    @property
    def all(self):
        return self.completed_win1 + self.completed_win2 + self.pending

    def __len__(self):
        return len(self.all)

    def _update_event(self, event: Event) -> None:
        event.state = random.choice(["win1", "win2"])
        if event.state == "win1":
            self.completed_win1.append(event)
        else:
            self.completed_win2.append(event)
        self.fifo_changes.put(event)

    def _update(self) -> None:
        _temp_pending = self.pending[:]
        for e_ind, event in enumerate(self.pending):
            if event.deadline < time.time() - self.delay:
                _temp_pending.remove(event)
                self._update_event(event)
        self.pending = _temp_pending

    def get_updates(self):
        self._update()
        while not self.fifo_changes.empty():
            yield self.fifo_changes.get()
        else:
            self.fifo_changes.task_done()
