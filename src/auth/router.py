import typing as tp
from fastapi import APIRouter, Depends
from src.dependencies import DatabaseMiddleware
from .models import User
from .schemas import UserCreate
from .service import PasswordManager


router = APIRouter(
    prefix="/auth",
)


@router.post("/register")
async def register(user: UserCreate, db=Depends(DatabaseMiddleware.get_session)):
    """
    Registers a new user in the database.

    Args:
        user (UserCreate): The user information to create.
        db (Session): The database session dependency.

    Returns:
        dict: A message indicating the user has been registered.
    """
    db.add(
        User(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            password=PasswordManager.hash_password(
                user.password
            ),  # TODO: hash password
        )
    )
    db.commit()
    # TODO: send email verification code
    # https://fastapi.tiangolo.com/tutorial/background-tasks/

    return {"message": "User registered"}


# TODO: Login
@router.post("/login")
async def login():
    return {"message": "User logged in"}
