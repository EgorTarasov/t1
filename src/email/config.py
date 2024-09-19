from pydantic_settings import BaseSettings
from contextvars import ContextVar


class EmailConfig(BaseSettings):
    mail_user: str
    mail_password: str
    host: str = "smtp.mail.ru"
    port: int = 465
    templates_path: str = "/templates"


email_config: ContextVar[EmailConfig] = ContextVar("email_config")
