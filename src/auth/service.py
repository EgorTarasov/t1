from passlib.context import CryptContext  # type: ignore
import hashlib
import datetime as dt
from typing import NamedTuple
from jose import jwt
from src.email.service import EmailClient
from src.config import app_config


class PasswordManager:
    pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return cls.pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def hash_password(cls, password: str) -> str:
        return cls.pwd_context.hash(password)


class CodeManager:

    @classmethod
    def get_verification_code(cls, email: str) -> str:
        return hashlib.md5((email + "id").encode())

    @classmethod
    def get_reset_code(cls, email: str) -> str:
        return hashlib.sha256((email + "reset").encode()).hexdigest()


def send_verification_code(
    client: EmailClient, email: str, verification_code: str
) -> None:

    subject = "Верификация аккаунта"
    template = "registration.jinja2"
    data = (
        {
            "verification_link": f"{app_config.get().domain}/email/verify{verification_code}"
            # TODO: Get route from router
        },
    )
    client.send_mailing(email, subject, template, data)
