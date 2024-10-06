from pydantic import Field, PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False, env_file=".env", extra="ignore"
    )
    docker_mode: bool = False

    logging: str = "DEBUG"

    postgres_dsn: PostgresDsn = Field(
        "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"
    )

    domain: str = "http://localhost:8000"


class WorkerConfig(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False, env_file=".env", extra="ignore"
    )
    redis_dsn: RedisDsn = Field("redis://localhost:6379/0")
    redis_db: int = 0

    postgres_dsn: PostgresDsn = Field(
        "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"
    )

    llm_chat_url: str = ""


app_config: Config = Config()  # type: ignore
