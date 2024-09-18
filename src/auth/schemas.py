from pydantic import BaseModel, Field, EmailStr


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
