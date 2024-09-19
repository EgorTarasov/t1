from .service import EmailClient
import typing as tp


class EmailClientMiddleware:
    email_client: EmailClient | None = None

    @staticmethod
    def set_email_client(email_client: EmailClient):
        EmailClientMiddleware.email_client = email_client

    @staticmethod
    async def get_client() -> tp.AsyncGenerator[EmailClient, None]:
        if EmailClientMiddleware.email_client is None:
            raise ValueError("Email client is not initialized")
        else:
            yield EmailClientMiddleware.email_client
