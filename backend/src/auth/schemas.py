import datetime as dt

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    """UserCreate

    Data required for email registration

    Args:
        BaseModel (_type_): _description_
    """

    first_name: str = Field("Egor", title="Имя")
    last_name: str = Field("Tarasov", title="Фамилия")
    email: EmailStr = Field(
        "@gmail.com", title="email", description="электронная почта"
    )
    password: str = Field("test12345678", min_length=12)


class UserLogin(BaseModel):
    email: EmailStr = Field(
        "@gmail.com", title="email", description="электронная почта"
    )
    password: str = Field("test12345678", min_length=12)


class EmailVerificationCodeDto(BaseModel):
    """EmailVerificationCodeDto

    Used for email verification template
    which contains url for verification
    """

    email: EmailStr
    code: str = Field("", min_length=128, max_length=128)


class AccessToken(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    access_token: str
    token_type: str = Field("Bearer")


class EmailRecovery(BaseModel):
    email: EmailStr = Field(
        "@gmail.com", title="email", description="электронная почта"
    )


class EmailRecoveryNewPassword(BaseModel):
    code: str = Field("", min_length=6, max_length=6)
    new_password: str = Field("test12345678", min_length=12)


class UserDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(1)
    first_name: str = Field("Egor", title="Имя")
    last_name: str = Field("Tarasov", title="Фамилия")
    email: EmailStr = Field(
        "@gmail.com", title="email", description="электронная почта"
    )
    role: str = Field("user")
    is_active: bool = Field(True)
    created_at: dt.datetime = Field("2021-01-01T00:00:00")
    updated_at: dt.datetime = Field("2021-01-01T00:00:00")
