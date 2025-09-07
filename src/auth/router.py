from fastapi import APIRouter, status
from fastapi.params import Depends
from src.auth.dependencies import validate_auth_user
from src.auth import utils as auth_utils
from .schemas import TokenInfo, UserSchema


router = APIRouter()


@router.post("/login/", response_model=TokenInfo)
async def auth_user_jwt(
    user: UserSchema = Depends(validate_auth_user)
):
    payload = {
        "sub": user.id,
        "username": user.username,
        "email": user.email,
    }
    token = auth_utils.encode_jwt(payload)
    return TokenInfo(
        access_token=token
    )


@router.post("/register/", status_code=status.HTTP_201_CREATED)
async def register_user():
    pass