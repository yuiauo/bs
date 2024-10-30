from functools import lru_cache
from pathlib import Path
from typing import Any
from yaml import safe_load


from pydantic_settings import BaseSettings, PydanticBaseSettingsSource, YamlConfigSettingsSource
# from pydantic import AmqpDsn, PostgresDsn


PARENT_DIR = Path(__file__).parent
APP_SETTINGS_PATH = Path(PARENT_DIR, "settings/app_config.yml")
LOG_SETTINGS_PATH = Path(PARENT_DIR, "settings/logging_config.yml")
ENV_PATH = Path(PARENT_DIR, "settings/.env")


class EnvSettings(BaseSettings, extra="allow", env_file=ENV_PATH):
    """Прочие настройки """
    # да, были наполеоновские планы добавить отдельную бд с паролями
    PEPPER: str
    RABBITMQ_URL: str
    EVENT_QUEUE: str = "events"
    PG_MIGRATIONS_URL: str
    PG_DATABASE_URL: str


@lru_cache
class AppSettings:
    """Синглтон для настроек"""
    def __init__(self):
        self.app = load_yaml(APP_SETTINGS_PATH)
        self.logger = load_yaml(LOG_SETTINGS_PATH)
        self.env = EnvSettings()


def load_yaml(path: Path) -> dict[str, Any]:
    with Path(path).open("r") as f:
        config = safe_load(f)
    if not isinstance(config, dict):
        raise FileNotFoundError("There is no appropriate file")
    return config


settings = AppSettings()
