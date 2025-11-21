from fastapi import APIRouter, status, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .dependencies import validate_auth_user, get_current_auth_user, get_current_user_for_refresh
from .schemas import TokenInfo, UserCreate, UserRegisteredResponse
from src.database import session_dependency
from src.models import User
from .services import auth_service as auth_service
from .services import token_service as token_service

router = APIRouter()


@router.post("/login/", response_model=TokenInfo)
async def auth_user_jwt(
        user: User = Depends(validate_auth_user)
):
    access_token = token_service.create_access_token(user)
    refresh_token = token_service.create_refresh_token(user)

    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post("/register/", status_code=status.HTTP_201_CREATED, response_model=UserRegisteredResponse)
async def register_user(
        user_data: UserCreate,
        session: AsyncSession = Depends(session_dependency)
):
    new_user = await auth_service.create_user(user_data, session)
    if not new_user:
        raise HTTPException(
            status_code=409,
            detail="User already exists",
        )

    return UserRegisteredResponse.model_validate({
        "id" : new_user.id,
        "username" : new_user.username,
        "email" : new_user.email
    })


@router.post("/refresh/", response_model=TokenInfo, response_model_exclude_none=True)
def refresh_jwt(
        user: User = Depends(get_current_user_for_refresh)
):
    access_token = token_service.create_access_token(user)
    return TokenInfo(
        access_token = access_token
    )


# For authorization valid working check
@router.get("/me/", response_model=UserRegisteredResponse)
async def get_me(
        user: User = Depends(get_current_auth_user)
):
    return UserRegisteredResponse.model_validate({
        "id": user.id,
        "username": user.username,
        "email": user.email
    })

