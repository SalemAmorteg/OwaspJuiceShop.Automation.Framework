from pydantic import BaseModel


class Authentication(BaseModel):
    token: str


class LoginResponse(BaseModel):
    authentication: Authentication