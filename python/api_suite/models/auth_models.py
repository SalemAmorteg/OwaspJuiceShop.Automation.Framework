from pydantic import BaseModel, EmailStr

class UserSchema(BaseModel):
    """
    Validates data structural requirements for User entity outputs returned via /api/Users.
    """
    id: int
    email: EmailStr
    createdAt: str
    updatedAt: str

class AuthenticationDetails(BaseModel):
    """
    Maps the internal validation parameters nested inside the 'authentication' key.
    """
    token: str
    bid: int
    umail: EmailStr

class LoginResponseSchema(BaseModel):
    """
    Top-level data contract validator mirroring the outer layer of the auth payload response.
    """
    authentication: AuthenticationDetails