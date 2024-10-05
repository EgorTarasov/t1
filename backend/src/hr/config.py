from pydantic_settings import BaseSettings, SettingsConfigDict


class HrConfig(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=".env",
        extra="ignore",
    )

    openai_api_key: str


hr_config = HrConfig()  # type: ignore
