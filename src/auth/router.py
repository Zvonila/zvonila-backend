from fastapi import APIRouter, Depends, HTTPException,  Header, Request
from typing import Annotated
from src.auth.schemas import UserLogin, TokenSchema, UserSchema, UserRegister
from src.auth.dependencies import get_auth_service
from src.auth.service import AuthService
from src.auth.exceptions import InvalidPasswordError, UserIsExist, UserCreateError, InvalidToken
from src.user.exceptions import UserNotFoundError
from src.sessions.exceptions import SessionNotFound, SessionIsNotYou
from src.auth.dependencies import verify_user

router = APIRouter()

@router.post("/login", response_model=TokenSchema)
async def login(
    form_data: UserLogin,
    request: Request,
    auth_service: AuthService = Depends(get_auth_service),
):
    try:
        return await auth_service.login_user(
            email=form_data.email, 
            password=form_data.password,
            ip="123",
            user_agent="123",
        )
    except (UserNotFoundError):
        print("Пользователь не найден")
        raise HTTPException(
            status_code=401,
            detail="Пользователь не найден",
        )
    except (InvalidPasswordError):
        print("Пароли не совпадают")
        raise HTTPException(
            status_code=401,
            detail="Пароли не совпадают",
        )

@router.post("/register", response_model=TokenSchema)
async def register(
    form_data: UserRegister,
    request: Request,
    auth_service: AuthService = Depends(get_auth_service),
):
    try:
        return await auth_service.register_user(
            email=form_data.email, 
            name=form_data.name,
            password=form_data.password,
            ip="123",
            user_agent="123",
        )
    except (UserIsExist):
        raise HTTPException(
            status_code=401,
            detail="Email уже занят",
        )
    except (InvalidPasswordError):
        raise HTTPException(
            status_code=401,
            detail="Пароли не совпадают",
        )
    except (UserCreateError):
        raise HTTPException(
            status_code=401,
            detail="Ошибка создания пользователя",
        )

@router.get("/verify", response_model=UserSchema)
async def verify(
    auth_service: AuthService = Depends(get_auth_service),
    user_id: int = Depends(verify_user),
):
    try:
        user = await auth_service._get_user_by_id(user_id=user_id,)
        return user
    except (InvalidToken):
        raise HTTPException(
            status_code=401,
            detail="Не валидный токен",
        )
    except (UserNotFoundError):
        raise HTTPException(
            status_code=401,
            detail="Пользователь не найден",
        )
    except (SessionNotFound):
        raise HTTPException(
            status_code=401,
            detail="Сессия не действительна",
        )

@router.post("/logout", response_model=None)
async def logout(
    authorization: Annotated[str | None, Header(include_in_schema=False)] = None,
    user_id: int = Depends(verify_user),
    auth_service: AuthService = Depends(get_auth_service),
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Заголовок авторизации не найден")
    
    access_token = authorization.removeprefix("Bearer ")
    print(access_token)
    try:
        await auth_service.logout(
            user_id=user_id,
            access_token=access_token,
        )
    except (SessionNotFound):
        print("Сессия не найдена")
        raise HTTPException(
            status_code=401,
            detail="Сессия не найдена",
        )
    except (SessionIsNotYou):
        print("Сессия не действительна")
        raise HTTPException(
            status_code=401,
            detail="Сессия не действительна",
        )
    except Exception as e:
        print(e)