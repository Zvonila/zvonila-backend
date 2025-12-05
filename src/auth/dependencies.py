from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.user.repository import UserRepository
from src.auth.service import AuthService
from src.user.dependencies import get_user_repository
from src.sessions.dependencies import get_session_service
from src.sessions.service import SessionService
from src.auth.utils import PasswordService, JWTService
from src.core.dependencies import get_jwt_service, get_password_service
from sqlalchemy.ext.asyncio import AsyncSession
from src.dependencies import get_db_session

def get_auth_service(
    db_session: AsyncSession = Depends(get_db_session),
    user_repo: UserRepository = Depends(get_user_repository),
    session_serv: SessionService = Depends(get_session_service),
    jwt_service: JWTService = Depends(get_jwt_service),
    password_service: PasswordService = Depends(get_password_service),
) -> AuthService:
    return AuthService(db_session, user_repo, session_serv, jwt_service, password_service)

bearer_scheme = HTTPBearer()

async def verify_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    auth_service: AuthService = Depends(get_auth_service),
) -> int:
    """
    Проверка токена и возврат user_id.
    Используется в Depends для эндпоинтов.
    """
    token = credentials.credentials

    try:
        user = await auth_service.verify_user(access_token=token)
        return user.id
    except Exception as err:
        print(err)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не авторизован",
        )