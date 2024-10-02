from celery import Celery
from src.dependencies import DatabaseMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from src.email.dependencies import EmailClientMiddleware
from src.email.service import EmailClient
import typing as tp
from src.hr.service import (
    HHApi,
    LLM,
)


app = Celery()
db: AsyncSession = Depends(DatabaseMiddleware.get_session)
app.conf.broker_url = "redis://10.0.1.80:6379/0"
app.conf.timezone = "UTC+3"


@app.task
def send_vacancy_mail(
    description: str,
    subject: str,
    user_name: str,
    email: str,
    client: EmailClient = Depends(EmailClientMiddleware.get_client),
) -> None:

    template = LLM.prompt("email", description)

    # client.send_mailing(email, subject, template)
