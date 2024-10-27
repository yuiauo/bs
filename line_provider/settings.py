from functools import lru_cache
from pydantic_settings import BaseSettings


@lru_cache(maxsize=1)
class APISettings(BaseSettings):
    title: str = "lp API"
    description: str = "Test task api N2"
    version: str = "1.0"
    debug: bool = True
    openapi_tags: list[dict] = [
        {"name": "Event", "description": "Event endpoints"},
    ]


settings = APISettings().model_dump()
