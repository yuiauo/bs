from functools import lru_cache
from typing import Any

from pydantic_settings import BaseSettings


class EnvSettings(BaseSettings):
    class Config:
        env_file = ".env"
        extra = "allow"


class PostgresSettings(EnvSettings):
    PG_PORT: int
    PG_HOST: str
    PG_DATABASE: str
    PG_USERNAME: str
    PG_PASSWORD: str


class APISettings(EnvSettings):
    title: str = "bs API"
    description: str = "Test task api"
    version: str = "1.0"
    debug: bool = True
    openapi_tags: list[dict] = [
        {"name": "User", "description": "User CRUD endpoints"},
        {"name": "Bet", "description": "Bet endpoints"},
        {"name": "Event", "description": "Event endpoints"},
    ]


class ExtraSettings(EnvSettings):
    PEPPER: str


@lru_cache(maxsize=1)
class Settings(BaseSettings):
    app: dict[str, Any]
    pg: PostgresSettings
    extra: ExtraSettings


settings = Settings(
    app=APISettings().model_dump(),
    pg=PostgresSettings(),
    extra=ExtraSettings(),
)
