import typing as tp
import datetime as dt

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.models import TimestampMixin

if tp.TYPE_CHECKING:
    from src.hr.models import Vacancy


class User(Base, TimestampMixin):
    __tablename__ = "users"  # type: ignore

    id: Mapped[int] = mapped_column(
        sa.Integer,
        primary_key=True,
        autoincrement=True,
    )
    first_name: Mapped[str] = mapped_column(
        sa.String(50),
        nullable=False,
    )
    last_name: Mapped[str] = mapped_column(
        sa.String(50),
        nullable=False,
    )
    email: Mapped[str] = mapped_column(
        sa.String(50),
        nullable=False,
        unique=True,
        index=True,
    )
    password: Mapped[str] = mapped_column(
        sa.Text,
        nullable=False,
    )

    role: Mapped[str] = mapped_column(
        sa.String(50),
        default="user",
        server_default="user",
        nullable=False,
    )
    secret: Mapped[str] = mapped_column(
        sa.String(50),
        nullable=False,
        server_default="",
    )

    verified: Mapped[bool] = mapped_column(
        sa.Boolean,
        default=False,
        nullable=False,
    )
    deleted_at: Mapped[dt.datetime] = mapped_column(
        default=None,
        server_default=None,
        nullable=True,
    )
    verification: Mapped["EmailVerificationCode"] = relationship(
        "EmailVerificationCode",
        back_populates="user",
        cascade="all,delete",
    )
    my_vacancies: Mapped[list["Vacancy"]] = relationship(
        "Vacancy",
        back_populates="hr",
        primaryjoin="Vacancy.hr_id == User.id",
        cascade="all,delete",
    )
    assigned_vacancies: Mapped[list["Vacancy"]] = relationship(
        "Vacancy",
        back_populates="recruiter",
        primaryjoin="Vacancy.recruiter_id == User.id",
        cascade="all,delete",
    )

    def __repr__(self):
        return f"<User {self.id}>"


class EmailVerificationCode(Base):
    """Code for verification email"""

    __tablename__ = "email_verification_codes"  # type: ignore

    fk_user_id: Mapped[int] = mapped_column(sa.ForeignKey("users.id"), primary_key=True)
    # generated on email registration
    code: Mapped[str] = mapped_column(sa.String(length=128), nullable=False)
    created_at: Mapped[dt.datetime] = mapped_column(default=dt.datetime.now())
    # change to timestamp when used
    used_at: Mapped[dt.datetime] = mapped_column(default=None, nullable=True)

    user: Mapped[User] = relationship(
        "User",
    )


class EmailRecoveryCode(Base):
    """Code for recovering email"""

    __tablename__ = "email_recovery_codes"  # type: ignore

    # TODO: Background job for expiring verification Code
    code: Mapped[str] = mapped_column(sa.String(6))
    fk_user_id: Mapped[int] = mapped_column(
        sa.ForeignKey("users.id"),
        primary_key=True,
    )
    user: Mapped[User] = relationship(
        "User",
    )
    created_at: Mapped[dt.datetime] = mapped_column(default=dt.datetime.now())
    # change to timestamp when used
    used_at: Mapped[dt.datetime] = mapped_column(default=None, nullable=True)
