from pydantic import (
    BaseModel,
    EmailStr,
    ConfigDict
)


class UserSchema(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: int
    email: EmailStr
    role: str


class RegistrationResponseSchema(BaseModel):
    model_config = ConfigDict(extra="ignore")

    status: str
    data: UserSchema


class AuthenticationSchema(BaseModel):
    model_config = ConfigDict(extra="ignore")

    token: str
    bid: int
    umail: EmailStr


class LoginResponseSchema(BaseModel):
    model_config = ConfigDict(extra="ignore")

    authentication: AuthenticationSchema

    @property
    def is_jwt(self) -> bool:
        return (
            self.authentication.token.count(".") == 2
        )


class ErrorResponseSchema(BaseModel):
    model_config = ConfigDict(extra="ignore")

    error: str