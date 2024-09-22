import typing as tp
import logging
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from src.dependencies import DatabaseMiddleware
from src.email.dependencies import EmailClientMiddleware
from .models import User, EmailVerificationCode, EmailRecoveryCode
from .schemas import (
    UserCreate,
    UserLogin,
    AccessToken,
    EmailRecovery,
    EmailRecoveryNewPassword,
)
import pyotp
from .service import (
    JWTEncoder,
    PasswordManager,
    CodeManager,
    send_recovery_code,
    send_verification_code,
)
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa
from sqlalchemy import orm
from src.email.service import EmailClient

router = APIRouter(
    prefix="/auth",
)


@router.post("/email/register")
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
        secret=pyotp.random_base32(),
    )
    try:
        db.add(db_user)
        await db.flush()
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=400, detail="Error while registering")

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

    #  TODO: return jwt token

    return {"message": "User registered"}


@router.get("/email/verify")
async def verify(
    code: str | None = None,
    db: AsyncSession = Depends(DatabaseMiddleware.get_session),
):
    invalid_request_exception = HTTPException(status_code=400, detail="Invalid request")

    if code is None:
        raise invalid_request_exception

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
        raise invalid_request_exception

    if user_code.used_at is not None:
        logging.info(f"Code {code} already used_at {user_code.used_at}")
        raise invalid_request_exception

    user_code.used_at = sa.func.now()
    user_code.user.verified = True
    try:
        await db.commit()
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=400, detail="Error while verifying user")

    return AccessToken(
        token_type="Bearer",
        access_token=JWTEncoder.create_access_token(
            user_code.user.id,
            user_code.user.role,
        ),
    )


# TODO: Login
@router.post("/email/login")
async def login(
    payload: UserLogin,
    db: AsyncSession = Depends(DatabaseMiddleware.get_session),
):

    stmt = sa.select(User).where(User.email == payload.email)
    user: User | None = (await db.execute(stmt)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not PasswordManager.verify_password(payload.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return AccessToken(
        token_type="Bearer",
        access_token=JWTEncoder.create_access_token(
            user.id,
            user.role,
        ),
    )


@router.post("/email/recover")
async def logout(
    payload: EmailRecovery,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(DatabaseMiddleware.get_session),
    email_client: EmailClient = Depends(EmailClientMiddleware.get_client),
):

    # 1. Create recovery code
    # 2. Send recovery code

    stmt = sa.select(User).where(User.email == payload.email)
    user: User | None = (await db.execute(stmt)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    code = CodeManager.get_recovery_code(user.secret)
    recovery_code = EmailRecoveryCode(fk_user_id=user.id, code=code)
    db.add(recovery_code)
    await db.commit()

    background_tasks.add_task(
        send_recovery_code,
        client=email_client,
        email=user.email,
        recovery_code=recovery_code.code,
        user_name=" ".join([user.first_name, user.last_name]),
    )

    return {"message": "Recovery code sent"}


@router.post("/email/reset")
async def reset(
    payload: EmailRecoveryNewPassword,
    db: AsyncSession = Depends(DatabaseMiddleware.get_session),
):
    invalid_credentials_exception = HTTPException(
        status_code=401, detail="Invalid credentials"
    )

    stmt = (
        sa.select(EmailRecoveryCode)
        .where(EmailRecoveryCode.code == payload.code)
        .options(orm.joinedload(EmailRecoveryCode.user))
    )
    code: EmailRecoveryCode | None = (await db.execute(stmt)).scalar_one_or_none()
    if code is None:
        logging.info(f"Code {payload.code} not found")
        raise invalid_credentials_exception

    if code.used_at is not None:
        logging.info(f"Code {payload.code} already used_at {code.used_at}")
        raise invalid_credentials_exception

    code.used_at = sa.func.now()

    if code.user is None:
        logging.info(f"User not found for code {payload.code}")
        raise invalid_credentials_exception

    code.user.password = PasswordManager.hash_password(payload.new_password)
    code.used_at = sa.func.now()
    await db.commit()

    return {"message": "Password reset"}
