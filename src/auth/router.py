import typing as tp
import logging
from fastapi import APIRouter, Depends, BackgroundTasks
from src.dependencies import DatabaseMiddleware
from src.email.dependencies import EmailClientMiddleware
from .models import User, EmailVerificationCode
from .schemas import UserCreate
from .service import PasswordManager, CodeManager, send_verification_code
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa
from sqlalchemy import orm
from src.email.service import EmailClient

router = APIRouter(
    prefix="/auth",
)


@router.post("/register")
async def register(
    user: UserCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(DatabaseMiddleware.get_session),
    email_client: EmailClient = Depends(EmailClientMiddleware.get_client),
):
    """
    Registers a new user in the database.

    Args:
        user (UserCreate): The user information to create.
        db (Session): The database session dependency.

    Returns:
        dict: A message indicating the user has been registered.
    """

    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=PasswordManager.hash_password(user.password),
    )
    db.add(db_user)
    await db.flush()

    code_object = EmailVerificationCode(
        fk_user_id=db_user.id,
        code=CodeManager.get_verification_code(db_user.email),
    )

    db.add(code_object)

    background_tasks.add_task(
        send_verification_code,
        client=email_client,
        email=user.email,
        verification_code=code_object.code,
        user_name=" ".join([user.first_name, user.last_name]),
    )

    await db.commit()
    # TODO: defines response schema
    return {"message": "User registered"}


@router.get("/email/verify")
async def verify(
    code: str | None = None,
    db: AsyncSession = Depends(DatabaseMiddleware.get_session),
):
    if code is None:
        return {"message": "Invalid request"}

    stmt = (
        sa.select(EmailVerificationCode)
        .where(EmailVerificationCode.code == code)
        .options(orm.joinedload(EmailVerificationCode.user))
    )

    user_code: EmailVerificationCode | None = (
        await db.execute(stmt)
    ).scalar_one_or_none()

    if user_code is None:
        logging.info(f"Code {code} not found")
        return {"message": "Invalid request"}

    if user_code.used_at is not None:
        logging.info(f"Code {code} already used_at {user_code.used_at}")
        return {"message": "Invalid request"}

    user_code.used_at = sa.func.now()
    user_code.user.verified = True
    await db.commit()

    return {"message": "User verified", "code": code}


# TODO: Login
@router.post("/login")
async def login():
    return {"message": "User logged in"}
