from pydantic import BaseModel, EmailStr


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"

class UserSchema(BaseModel):
    id: int
    username: str
    password: str
    email: EmailStr
    role: str

class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr

class UserRegisteredResponse(BaseModel):
    id: int
    username: str
    email: EmailStr


