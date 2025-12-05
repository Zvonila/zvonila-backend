from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.dependencies import get_db_session
from src.user.repository import UserRepository
from src.user.service import UserService
from src.auth.utils import PasswordService
from src.core.dependencies import get_password_service

def get_user_repository(session: AsyncSession = Depends(get_db_session)) -> UserRepository:
    return UserRepository(session)

def get_user_service(
    db_session: AsyncSession = Depends(get_db_session),
    user_repo: UserRepository = Depends(get_user_repository),
    password_service: PasswordService = Depends(get_password_service),  
) -> UserService:
    return UserService(db_session, user_repo, password_service)
