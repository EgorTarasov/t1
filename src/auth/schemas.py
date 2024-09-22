from pydantic import BaseModel, Field, EmailStr, ConfigDict


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
