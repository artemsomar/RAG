from fastapi import HTTPException, status, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .utils import validate_password
from src.auth.schemas import AuthUser
from src.models import User
from ..database import session_dependency


async def validate_auth_user(user: AuthUser, session: AsyncSession = Depends(session_dependency)) -> User:
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
    )
    db_user_result = await session.execute(select(User).where(User.username == user.username))
    db_user: User = db_user_result.scalars().first()
    if not db_user:
        raise unauthed_exc

    if validate_password(user.password, db_user.password_hash):
        return db_user

    raise unauthed_exc
