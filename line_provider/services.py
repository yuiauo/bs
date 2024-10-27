import asyncio
import os
from typing import AsyncGenerator

import aio_pika
from aio_pika.abc import AbstractChannel
from dotenv import load_dotenv

from line_provider.main import EVENT_QUEUE
from schemas import Event


load_dotenv()
RABBITMQ_URL = os.getenv("RABBITMQ_URL")
EVENT_QUEUE = "events"

# async def get_db() -> AsyncGenerator[AbstractConnection, None]:
#     connection = await aio_pika.connect(RABBITMQ_URL)
#     channel = await connection.channel()
#     queue = await channel.declare_queue(EVENT_QUEUE, durable=True)
#     try:
#         yield queue
#     finally:
#         await channel.close()
#         await connection.close()

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


async def send_multiple_events(
        events: list[Event],
        channel: AbstractChannel) -> None:
    tasks = [send_event(event, channel) for event in events]
    await asyncio.gather(*tasks)
