from pydantic_settings import BaseSettings


class PostgresSettings(BaseSettings):
    PG_PORT: int
    PG_HOST: str
    PG_DATABASE: str
    PG_USERNAME: str
    PG_PASSWORD: str

    class Config:
        env_file = ".env"
        extra = "allow"


class APISettings(BaseSettings):
    PEPPER: str

    class Config:
        env_file = ".env"
        extra = "allow"


class Settings(BaseSettings):
    app: APISettings
    pg: PostgresSettings

settings = Settings(
    app=APISettings(),
    pg=PostgresSettings(),
)
