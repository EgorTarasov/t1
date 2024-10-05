import datetime as dt
import typing as tp

import pyotp
import sqlalchemy as sa
from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    HTTPException,
    Request,
    Header,
    Query,
)
from loguru import logger
from sqlalchemy import orm
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import get_db
from src.email.dependencies import get_email
from src.email.service import EmailClient

from .models import EmailRecoveryCode, EmailVerificationCode, User
from .schemas import (
    AccessToken,
    EmailRecovery,
    EmailRecoveryNewPassword,
    UserCreate,
    UserDto,
    UserLogin,
)
from .service import (
    CodeManager,
    JWTEncoder,
    PasswordManager,
    send_recovery_code,
    send_verification_code,
)

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/email/register")
async def register(
    user: UserCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    email_client: EmailClient = Depends(get_email),
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
        logger.error(e)
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
    await db.refresh(db_user, ["id"])
    # TODO: defines response schema

    #  TODO: return jwt token

    return AccessToken(
        token_type="Bearer",
        access_token=JWTEncoder.create_access_token(
            db_user.id,
            db_user.role,
        ),
    )


@router.get("/email/verify")
async def verify(
    code: str | None = None,
    db: AsyncSession = Depends(get_db),
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
        logger.info(f"Code {code} not found")
        raise invalid_request_exception

    if user_code.used_at is not None:
        logger.info(f"Code {code} already used_at {user_code.used_at}")
        raise invalid_request_exception

    user_code.used_at = sa.func.now()
    user_code.user.verified = True
    try:
        await db.commit()
    except Exception as e:
        logger.error(e)
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
    db: AsyncSession = Depends(get_db),
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
    db: AsyncSession = Depends(get_db),
    email_client: EmailClient = Depends(get_email),
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
    db: AsyncSession = Depends(get_db),
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
        logger.info(f"Code {payload.code} not found")
        raise invalid_credentials_exception

    if code.used_at is not None:
        logger.info(f"Code {payload.code} already used_at {code.used_at}")
        raise invalid_credentials_exception

    code.used_at = dt.datetime.now()

    if code.user is None:
        logger.info(f"User not found for code {payload.code}")
        raise invalid_credentials_exception

    code.user.password = PasswordManager.hash_password(payload.new_password)
    code.used_at = dt.datetime.now()
    await db.commit()

    return {"message": "Password reset"}


@router.get("/me")
async def me(
    token: str | None = Query(None),
    authorization: tp.Annotated[str | None, Header()] = None,
    db: AsyncSession = Depends(get_db),
) -> UserDto:
    """
    Retrieves the current authenticated user's information.

    """
    # Read bearer token from headers and search user with id
    print(authorization, token)
    if authorization is None and token is None:
        raise HTTPException(
            status_code=401, detail="Authorization header missing or invalid"
        )
    if token is not None:
        if len(token.split(" ")) != 2:
            raise HTTPException(
                status_code=401, detail="Authorization header missing or invalid"
            )
        token = token.split(" ")[1]
    elif authorization is not None:
        if len(authorization.split(" ")) != 2:
            raise HTTPException(
                status_code=401, detail="Authorization header missing or invalid"
            )
        token = authorization.split(" ")[1]

    try:

        payload = JWTEncoder.decode_access_token(token)
        stmt = sa.select(User).where(User.id == payload.user_id)
        user: User | None = (await db.execute(stmt)).scalar_one_or_none()
        print(payload)
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return UserDto.model_validate(user)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=401, detail="Invalid token")
