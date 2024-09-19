import typing as tp
from pydantic_settings import BaseSettings, SettingsConfigDict
from contextvars import ContextVar
import logging


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        # env_file_encoding="utf-8", env_file="../../dev.env"
    )

    logging: str = "DEBUG"

    postgres_host: str
    postgres_port: int = 5432
    postgres_db: str

    postgres_user: str
    postgres_password: str

    vk_client_id: str
    vk_secure_token: str
    vk_service_token: str
    vk_redirect_uri: str = "http://localhost:5173/login"

    vk_token_url: str = (
        "https://oauth.vk.com/access_token?client_id={client_id}&client_secret={vk_secure_token}&redirect_uri={redirect_uri}&code={code}"
    )
    vk_base_url: str = "https://api.vk.ru/method"

    @property
    def postgres_dsn(self) -> str:
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

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


app_config: ContextVar[Config] = ContextVar("config")
