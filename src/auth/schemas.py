from pydantic import BaseModel, EmailStr


class TokenInfo(BaseModel):
    access_token: str
    token_type: str = "Bearer"


class UserLogin(BaseModel):
    username: str
    password: str


class UserBase(BaseModel):
    username: str
    password: str
    email: EmailStr


class UserSchema(UserBase):
    id: int


class UserCreate(UserBase):
    pass


