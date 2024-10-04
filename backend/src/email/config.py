from pydantic_settings import BaseSettings, SettingsConfigDict


class EmailConfig(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=".env",
        extra="ignore",
    )

    mail_user: str
    mail_password: str
    host: str = "smtp.mail.ru"
    port: int = 465
    templates_path: str = "templates"


email_config: EmailConfig = EmailConfig()  # type: ignore
