from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.schemas import UserCreate
from src.auth.utils import validate_password, hash_password
from src.models import User


async def authenticate_user(
        username: str,
        password: str,
        session: AsyncSession,
) -> User | None:
    result = await session.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    if not user:
        return None
    if not validate_password(password, user.password_hash):
        return None
    return user


async def get_user_by_id(
        user_id: int,
        session: AsyncSession,
) -> User | None:
    result = await session.execute(select(User).where(User.id == user_id))
    return result.scalars().first()


async def create_user(
        user_data: UserCreate,
        session: AsyncSession,
) -> User | None:
    existing_user = await session.execute(
        select(User).where(
            or_(
                User.username == user_data.username,
                User.email == user_data.email
            )
        )
    )
    if existing_user.scalar_one_or_none():
        return None
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        role="user",
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user
