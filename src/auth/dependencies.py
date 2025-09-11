from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .utils import validate_password, decode_jwt
from src.auth.schemas import UserLogin
from src.models import User
from ..database import session_dependency


async def validate_auth_user(
        user: UserLogin,
        session: AsyncSession = Depends(session_dependency)
) -> User:
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
    )
    db_user_result = await session.execute(select(User).where(User.username == user.username))
    db_user = db_user_result.scalars().first()
    if not db_user or not validate_password(user.password, db_user.password_hash):
        raise unauthed_exc
    return db_user


async def get_user_by_token(
        credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer),
        session: AsyncSession = Depends(session_dependency),
) -> User:
    token = credentials.credentials
    try:
        payload: dict = decode_jwt(token)
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token error: {e}",
        )
    db_user_result = await session.execute(select(User).where(User.id == payload.get("sub")))
    db_user = db_user_result.scalars().first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalid",
        )
    return db_user