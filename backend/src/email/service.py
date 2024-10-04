import pathlib
import smtplib
import typing as tp
from email.mime.text import MIMEText

import jinja2
from loguru import logger

from src.email.config import email_config


class EmailData(tp.TypedDict):
    to: str
    subject: str
    template: str
    data: dict[str, tp.Any]


class EmailClient:
    def __init__(
        self,
        mail_user: str,
        mail_password: str,
        host: str = "smtp.mail.ru",
        port: int = 465,
        templates_path: pathlib.Path | str = pathlib.Path("templates"),
    ) -> None:
        """EmailClient для отправки писем через smtp сервер

        Реализует возможность email рассылки через smtp сервер

        Для писем используется шаблоны jinja2

        Args:
            mail_user (str): почтовый ящик, с которого будут отправляться письма
            mail_password (str): пароль от почтового ящика
            server_host (str, optional): host для smtp сервера По умолчанию "smtp.mail.ru".
            server_port (int, optional): _description_. По умолчанию 587.
            templates_path (pathlib.Path | str, optional): путь до папки с шаблонами писем. По умолчанию pathlib.Path("./templates").
        """

        self._host = host
        self._port = port
        self.__user = mail_user
        self.__password = mail_password
        self._templates = jinja2.Environment(
            loader=jinja2.FileSystemLoader(templates_path)
        )
        if len(self._templates.list_templates()) == 0:
            raise ValueError("No templates found")
        logger.info("Email client initialized")

    def _create_connection(self) -> smtplib.SMTP_SSL:

        server = smtplib.SMTP_SSL(self._host, self._port)
        try:
            reply = server.login(self.__user, self.__password)
            logger.debug(reply)
        except Exception as e:
            logger.error(f"Can't connect to mail server: {e}")
            raise e
        finally:
            logger.info("Connected to mail server")
        return server

    def send_mailing(
        self,
        to: str,
        subject: str,
        template: str,
        data: dict[str, tp.Any],
    ) -> None:
        """Отправка письма через SMTP

        Args:
            to (str): почтовый адрес получателя
            subject (str): Тема письма
            template (str): Название шаблона
            data (dict[str, Any]): Данные для отрисовки шаблона

        Raises:
            e: Ошибка создание шаблона / соединения с сервером
        """
        server = self._create_connection()
        logger.debug(
            f"sending, to: {to}, subject: {subject}, template: {template}, data: {data}"
        )

        try:
            msg = MIMEText(
                self._templates.get_template(f"{template}.html").render(**data),
                "html",
            )
            msg["To"] = to
            msg["Subject"] = subject
            send_errs = server.sendmail(self.__user, to, msg.as_string())
            if send_errs:
                logger.error(send_errs)
        except Exception as e:
            logger.error(f"Can't send email: {e}")

            raise e
        server.close()


email_client = EmailClient(**dict(email_config))
