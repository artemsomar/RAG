from fastapi import HTTPException, status, Depends, Form
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.utils import decode_jwt
from src.database.models import User
from src.database.session import session_dependency
from src.auth.services import auth_service

http_bearer = HTTPBearer()


async def validate_auth_user(
    username: str = Form(),
    password: str = Form(),
    session: AsyncSession = Depends(session_dependency),
) -> User:
    user = await auth_service.authenticate_user(username, password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    return user


async def get_current_token_payload(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
):
    token = credentials.credentials
    try:
        payload: dict = decode_jwt(token)
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {e}",
        )
    return payload


def __validate_token_type(payload: dict, token_type: str) -> bool:
    current_token_type = payload.get("type")
    if current_token_type == token_type:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Invalid token type {current_token_type!r}, expected {token_type!r}",
    )


async def __get_current_user_by_payload(payload: dict, session: AsyncSession) -> User:
    user = await auth_service.get_user_by_id(int(payload.get("sub")), session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalid",
        )
    return user


async def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(session_dependency),
) -> User:
    __validate_token_type(payload, "access")
    user = await __get_current_user_by_payload(payload, session)
    return user


async def get_current_user_for_refresh(
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(session_dependency),
) -> User:
    __validate_token_type(payload, "refresh")
    user = await __get_current_user_by_payload(payload, session)
    return user
