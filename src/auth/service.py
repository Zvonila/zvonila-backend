from datetime import datetime
from src.user.repository import UserRepository
from src.auth.utils import PasswordService, JWTService
from src.auth.exceptions import InvalidPasswordError, UserIsExist, UserCreateError, InvalidToken
from src.user.exceptions import UserNotFoundError
from src.auth.schemas import TokenSchema, UserSchema
from src.sessions.service import SessionService
from src.sessions.exceptions import SessionNotFound
from typing import Dict, cast, Optional
from src.dependencies import transactional
from sqlalchemy.ext.asyncio import AsyncSession

class AuthService:
    """Сервис для аутентификации и регистрации пользователей"""

    def __init__(
            self, 
            db_session: AsyncSession,
            user_repo: UserRepository, 
            session_serv: SessionService,
            jwt_serv: JWTService,
            password_serv: PasswordService,
        ):
        self.user_repo = user_repo
        self.session_serv = session_serv
        self.jwt_service = jwt_serv
        self.password_service = password_serv
        self.db_session = db_session

    @transactional
    async def login_user(self, email: str, password: str, ip: str, user_agent: str) -> TokenSchema:
        """Аутентификация пользователя и создание сессии"""
        user = await self._get_user_by_email(email)
        self._verify_password(cast(str, user.password), password)

        now = datetime.now()
        claims = self._generate_claims(user, now)
        jwt_token = self.jwt_service.generate(claims)

        await self.session_serv.create_session(
            user_id=cast(int, user.id), 
            token=jwt_token,
            ip=ip,
            user_agent=user_agent,
            created_at=now,
        )
        return TokenSchema(token_type="bearer", access_token=jwt_token)
    

    # Нужно будет удалить, мы не поддерживаем прямую регистрацию
    @transactional
    async def register_user(self, email: str, name: str, password: str, ip: str, user_agent: str) -> TokenSchema:
        """Регистрация нового пользователя и генерация токена"""
        if await self.user_repo.find_user_by_email(email):
            raise UserIsExist()

        hashed = self.password_service.hash(password)
        user = await self.user_repo.add_user(email, name, hashed)
        if not user:
            raise UserCreateError()

        now = datetime.now()
        claims = self._generate_claims(user)
        jwt_token = self.jwt_service.generate(claims)
        
        await self.session_serv.create_session(
            user_id=cast(int, user.id),
            token=jwt_token,
            ip=ip,
            user_agent=user_agent,
            created_at=now,
        )

        return TokenSchema(token_type="bearer", access_token=jwt_token)
    
    @transactional
    async def verify_user(self, access_token: str) -> UserSchema:
        """Верификация JWT токена и существующей сессии"""
        data = self.jwt_service.decode(access_token)
        user_id = data.get("id")
        if not user_id:
            raise InvalidToken()

        user = await self._get_user_by_id(user_id)
        await self._get_session_or_raise(access_token)
        return UserSchema.model_validate(user)
    
    @transactional
    async def logout(self, user_id: int, access_token: str) -> None:
        """Удаление сессии пользователя"""
        session = await self._get_session_or_raise(access_token)
        await self.session_serv.delete_session(session_id=cast(int, session.id), user_id=user_id)
    
    
    # Приватные методы для уменьшения кода сервисов
    async def _get_user_by_email(self, email: str):
        user = await self.user_repo.find_user_by_email(email)
        if not user:
            raise UserNotFoundError()
        return user
    
    def _verify_password(self, hashed: str, raw: str) -> None:
        if not self.password_service.verify(hashed, raw):
            raise InvalidPasswordError()
        
    def _generate_claims(self, user, now: Optional[datetime] = None) -> Dict:
        now = now or datetime.now()
        return {"id": user.id, "email": user.email, "created_at": now.isoformat()}
    
    async def _get_user_by_id(self, user_id: int):
        user = await self.user_repo.find_user_by_id(user_id)
        if not user:
            raise UserNotFoundError()
        return user
    
    async def _get_session_or_raise(self, access_token: str):
        session = await self.session_serv.verify_session(access_token)
        if not session:
            raise SessionNotFound()
        return session
