from functools import wraps
from typing import Any, Callable

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from logger import logger


def handle_exception(func: Callable[[Request], Any]):
    @wraps(func)
    async def wrapped(*args, **kwargs) -> Callable[[Request], Any]:
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logger.exception(e)
            db: AsyncSession | None = kwargs.get('db')
            if db is not None:
                await db.rollback()
    return wrapped
