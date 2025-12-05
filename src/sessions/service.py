from datetime import datetime
from src.sessions.repository import SessionRepository
from src.sessions.exceptions import SessionCreateError, SessionNotFound, SessionIsNotYou
from typing import Optional, cast
from src.dependencies import transactional
from sqlalchemy.ext.asyncio import AsyncSession
from collections.abc import Sequence
from src.sessions.schemas import SessionSchema

class SessionService:
    """Сервис для управления пользовательскими сессиями"""

    def __init__(self, db_session: AsyncSession, session_repo: SessionRepository):
        self.session_repo = session_repo
        self.db_session = db_session

    @transactional
    async def create_session(
            self, 
            user_id: int, 
            token: str, 
            ip: str, 
            user_agent: str,
            created_at: datetime,
    ) -> SessionSchema:
        """Создает новую сессию для пользователя"""
        session = await self.session_repo.add_session(
            user_id=user_id,
            token=token,
            ip=ip,
            user_agent=user_agent,
            created_at=created_at,
        )

        if not session:
            raise SessionCreateError()

        return SessionSchema.model_validate(session)
    
    @transactional
    async def _get_session_or_raise(self, session_id: int, user_id: Optional[int] = None) -> SessionSchema:
        """Получает сессию и проверяет права доступа (если указан user_id)"""
        session = await self.session_repo.get_session_by_id(session_id)
        if not session:
            raise SessionNotFound()
        if user_id is not None and cast(int, session.user_id) != user_id:
            raise SessionIsNotYou()
        return SessionSchema.model_validate(session)
    
    @transactional
    async def delete_session(self, session_id: int, user_id: int) -> None:
        """Удаляет сессию пользователя"""
        await self._get_session_or_raise(session_id, user_id)
        await self.session_repo.delete_session(session_id)

    @transactional
    async def get_session_by_id(self, session_id: int) -> Optional[SessionSchema]:
        """Возвращает сессию по ID"""
        session_obj = await self.session_repo.get_session_by_id(session_id)
        if not session_obj:
            return None
        
        return SessionSchema.model_validate(session_obj) 

    @transactional
    async def get_user_sessions(self, user_id: int) -> Sequence[SessionSchema]:
        """Возвращает все сессии пользователя"""
        return [SessionSchema.model_validate(session) for session in await self.session_repo.get_user_sessions(user_id)]

    @transactional
    async def verify_session(self, access_token: str) -> Optional[SessionSchema]:
        """Проверяет наличие сессии по токену"""
        session_obj = await self.session_repo.get_session_by_token(access_token)
        if not session_obj:
            return None
        
        return SessionSchema.model_validate(session_obj) 