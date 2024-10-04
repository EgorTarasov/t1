from celery import Celery

from src.config import WorkerConfig
from src.database import Database
from src.email.config import EmailConfig
from src.email.service import EmailClient
from src.hr.service import LLM, HHApi

worker_config = WorkerConfig()  # type: ignore
email_config = EmailConfig()  # type: ignore
pg: Database = Database(str(worker_config.postgres_dsn))
email: EmailClient = EmailClient(
    email_config.mail_user,
    email_config.mail_password,
    email_config.host,
    email_config.port,
)
app: Celery = Celery(broker=str(worker_config.redis_dsn))
hh_api = HHApi()
llm = LLM()


@app.task
def send_vacancy_mail(
    description: str,
    subject: str,
    user_name: str,
    email: str,
) -> None:

    template = LLM.prompt("email", description)
    print(template)
    # client.send_mailing(email, subject, template)
