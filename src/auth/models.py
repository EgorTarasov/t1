from src import Base
from src.models import TimestampMixin
from sqlalchemy.orm import relationship, mapped_column, Mapped
import sqlalchemy as sa
from datetime import datetime


class User(Base, TimestampMixin):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(sa.String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(sa.String(50), nullable=False)
    email: Mapped[str] = mapped_column(
        sa.String(50), nullable=False, unique=True, index=True
    )
    password: Mapped[str] = mapped_column(sa.Text, nullable=False)

    role: Mapped[str] = mapped_column(
        sa.String(50), default="user", server_default="user", nullable=False
    )
    secret: Mapped[str] = mapped_column(
        sa.String(50), nullable=False, server_default=""
    )

    verified: Mapped[bool] = mapped_column(sa.Boolean, default=False, nullable=False)
    deleted_at: Mapped[datetime] = mapped_column(
        default=None, server_default=None, nullable=True
    )
    verification: Mapped["EmailVerificationCode"] = relationship(
        "EmailVerificationCode", back_populates="user"
    )

    def __repr__(self):
        return f"<User {self.id}>"


class EmailVerificationCode(Base):
    # TODO: Background job for expiring verification Code
    fk_user_id: Mapped[int] = mapped_column(sa.ForeignKey("users.id"), primary_key=True)
    # generated on email registration
    code: Mapped[str] = mapped_column(sa.String(128), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=sa.func.now())
    # change to timestamp when used
    used_at: Mapped[datetime] = mapped_column(default=None, nullable=True)

    user: Mapped[User] = relationship("User")


class EmailRecoveryCode(Base):
    # TODO: Background job for expiring verification Code
    code: Mapped[str] = mapped_column(sa.String(6))
    fk_user_id: Mapped[int] = mapped_column(sa.ForeignKey("users.id"), primary_key=True)
    user: Mapped[User] = relationship("User")
    created_at: Mapped[datetime] = mapped_column(server_default=sa.func.now())
    # change to timestamp when used
    used_at: Mapped[datetime] = mapped_column(default=None, nullable=True)
