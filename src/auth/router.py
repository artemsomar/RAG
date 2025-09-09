from fastapi import APIRouter, status, HTTPException
from fastapi.params import Depends
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependencies import validate_auth_user
from src.auth import utils as auth_utils
from .schemas import TokenInfo, UserSchema, UserCreate
from .utils import hash_password
from ..database import session_dependency
from ..models import User

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
async def register_user(
        user: UserCreate,
        session: AsyncSession = Depends(session_dependency)
):
    existing_user = await session.execute(
        select(User).where(
            or_(
                User.username == user.username,
                User.email == user.email,
            )
        )
    )
    if existing_user.scalar_one_or_none():
        raise HTTPException(
            status_code=409,
            detail="User already exists",
        )
    new_user = User(
        username=user.username,
        email=user.email,
        password_hash=hash_password(user.password),
        role="user",
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return {
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email,
    }


