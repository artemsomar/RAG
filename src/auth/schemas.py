from pydantic import BaseModel, EmailStr


class TokenInfo(BaseModel):
    access_token: str
    token_type: str = "Bearer"


class AuthUser(BaseModel):
    username: str
    password: str


class UserSchema(BaseModel):
    id: int
    username: str
    password: str
    email: EmailStr

