from functools import lru_cache

from pydantic_settings import BaseSettings
from pydantic import AmqpDsn


class APISettings(BaseSettings):
    title: str = "bs API"
    description: str = "Test task api"
    version: str = "1.0"
    debug: bool = True
    openapi_tags: list[dict] = [
        {"name": "User", "description": "User CRUD endpoints"},
        {"name": "Bet", "description": "Bet endpoints"},
        {"name": "Event", "description": "Event endpoints"},
    ]


class ExtraSettings(BaseSettings, extra="allow", env_file=".env"):
    PEPPER: str
    # раббит с урлом не рабит
    # RABBITMQ_URL: AmqpDsn
    RABBITMQ_URL: str
    EVENT_QUEUE: str = "events"

@lru_cache
class AppSettings:
    def __init__(self):
        self.api = APISettings().model_dump()
        self.extra = ExtraSettings()


settings = AppSettings()
