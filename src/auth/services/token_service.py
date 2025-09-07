from fastapi import HTTPException, status

from src.auth import utils as auth_utils
from src.config import settings
from src.models import User


def create_access_token(
        user: User
) -> str:
    payload = {
        "type": "access",
        "sub": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role,
    }
    access_token = auth_utils.encode_jwt(
        payload=payload,
        expires_minutes=settings.auth.access_token_expires_minutes,
    )
    return access_token


def create_refresh_token(
        user: User
) -> str:
    payload = {
        "type": "refresh",
        "sub": user.id,
    }
    refresh_token = auth_utils.encode_jwt(
        payload=payload,
        expires_minutes=settings.auth.refresh_token_expires_minutes,
    )
    return refresh_token
