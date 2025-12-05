from fastapi import APIRouter, Depends, HTTPException
from src.auth.dependencies import verify_user
from src.user.schemas import ChangePasswordRequest, ChangeNameRequest
from src.user.service import UserService
from src.user.dependencies import get_user_service
from src.user.exceptions import UserNotFoundError
from src.auth.exceptions import InvalidPasswordError
from typing import List
from src.auth.schemas import UserSchema
from collections.abc import Sequence

router = APIRouter()

@router.put("/change-password")
async def change_password(
    form_data: ChangePasswordRequest,
    user_id: int = Depends(verify_user),
    user_service: UserService = Depends(get_user_service),
):
    try:
        await user_service.change_password(
            user_id=user_id,
            password=form_data.password,
            new_password=form_data.new_password,
        )
    except (UserNotFoundError):
        raise HTTPException(
            status_code=500,
            detail="Пользователь не найден",
)
    except (InvalidPasswordError):
        raise HTTPException(
            status_code=500,
            detail="Не валидный пароль",
        )

    return None

@router.put("/change-name")
async def change_name(
    form_data: ChangeNameRequest,
    user_id: int = Depends(verify_user),
    user_service: UserService = Depends(get_user_service),
):
    try:
        await user_service.change_name(
            user_id=user_id,
            name=form_data.name,
        )
    except (UserNotFoundError):
        raise HTTPException(
            status_code=500,
            detail="Пользователь не найден",
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Произошла ошибка",
        )

    return None

@router.get("/", response_model=Sequence[UserSchema])
async def get_users(
    user_id: int = Depends(verify_user),
    user_service: UserService = Depends(get_user_service),
):
    try:
        return await user_service.get_users()
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Произошла ошибка",
        )
    

@router.get("/{id}", response_model=UserSchema)
async def get_user(
    id: int,
    user_id: int = Depends(verify_user),
    user_service: UserService = Depends(get_user_service),
):
    try:
        return await user_service.get_user_by_id(id)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Произошла ошибка",
        )