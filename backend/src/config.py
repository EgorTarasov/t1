import logging
from contextvars import ContextVar

from pydantic import Field, PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
    )
    docker_mode: bool = False

    logging: str = "DEBUG"

    postgres_dsn: PostgresDsn = Field(
        "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"
    )

    domain: str = "http://localhost:8000"

    vk_client_id: str
    vk_secure_token: str
    vk_service_token: str
    vk_redirect_uri: str = "http://localhost:5173/login"

    vk_token_url: str = (
        "https://oauth.vk.com/access_token?client_id={client_id}&client_secret={vk_secure_token}&redirect_uri={redirect_uri}&code={code}"
    )
    vk_base_url: str = "https://api.vk.ru/method"

    @property
    def logging_level(self):
        levels = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
        }
        return levels.get(self.logging.upper(), logging.INFO)


class WorkerConfig(BaseSettings):
    redis_dsn: RedisDsn = Field("redis://localhost:6379/0")
    redis_db: int = 0

    postgres_dsn: PostgresDsn = Field(
        "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"
    )

    llm_chat_url: str = ""


app_config: ContextVar[Config] = ContextVar("config")
