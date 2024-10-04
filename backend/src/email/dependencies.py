import typing as tp

from src.email.service import EmailClient, email_client


async def get_email() -> tp.AsyncGenerator[EmailClient, None]:
    """Dependency for getting email client"""
    if email_client is None:
        raise ValueError("Email client is not initialized")
    else:
        yield email_client
