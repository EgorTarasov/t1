import datetime as dt
import hashlib
import typing as tp
from typing import NamedTuple

import pyotp
from jose import jwt
from passlib.context import CryptContext  # type: ignore

from src.config import app_config
from src.email.service import EmailClient


class UserTokenData(NamedTuple):
    """Данные которые хранятся в jwt токене пользователя
    user_id: int
    email: str

    exp: dt.datetime
    """

    user_id: int
    role: str
    exp: dt.datetime


class JWTEncoder:
    jwt_secret_key: str = "fjdlasjroj3oi4o12j4oi3j1oi4nguoda"
    jwt_algorithm: str = "HS256"
    jwt_hash_algorithm: str = "HS256"

    @classmethod
    def set_secret_key(cls, secret_key: str) -> None:
        cls.jwt_secret_key = secret_key

    @classmethod
    def create_jwt_token(
        cls,
        data: dict[str, str | dt.datetime | int],
        expires_delta: dt.timedelta = dt.timedelta(days=1),
    ):
        to_encode: dict[str, dt.datetime | tp.Any] = data.copy()
        to_encode["exp"] = dt.datetime.now() + expires_delta
        return jwt.encode(to_encode, cls.jwt_secret_key, algorithm=cls.jwt_algorithm)

    @classmethod
    def decode_jwt(cls, token: str) -> dict[str, str | dt.datetime]:
        return jwt.decode(token, cls.jwt_secret_key, cls.jwt_hash_algorithm)

    @classmethod
    def create_access_token(
        cls,
        user_id: int,
        role: str,
        expires_delta: dt.timedelta = dt.timedelta(days=1),
    ) -> str:
        to_encode: dict[str, tp.Any] = {
            "user_id": user_id,
            "role": role,
            "exp": dt.datetime.now() + expires_delta,
        }
        return jwt.encode(
            to_encode, cls.jwt_secret_key, algorithm=cls.jwt_hash_algorithm
        )

    @classmethod
    def decode_access_token(cls, token: str) -> UserTokenData:
        return UserTokenData(
            **jwt.decode(token, cls.jwt_secret_key, cls.jwt_hash_algorithm)
        )


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
    def get_recovery_code(cls, secret: str) -> str:
        return pyotp.TOTP(secret, interval=300).now()

    @classmethod
    def get_verification_code(cls, email: str) -> str:
        return hashlib.sha256((email + "reset").encode()).hexdigest()


def send_verification_code(
    client: EmailClient, email: str, verification_code: str, user_name: str
) -> None:

    subject = "Верификация аккаунта"
    template = "email/verification.jinja2"
    data: dict[str, tp.Any] = {
        "user_name": user_name,
        "verification_url": f"{app_config.get().domain}/auth/email/verify",
        "verification_code": verification_code,
    }

    client.send_mailing(email, subject, template, data)


def send_recovery_code(
    client: EmailClient, email: str, recovery_code: str, user_name: str
) -> None:

    subject = "Восстановление аккаунта"
    template = "email/recovery.jinja2"
    data: dict[str, tp.Any] = {
        "user_name": user_name,
        "recovery_url": f"{app_config.get().domain}/auth/email/recovery",
        "recovery_code": recovery_code,
    }

    client.send_mailing(email, subject, template, data)
