from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, delete
from datetime import datetime
from src.sessions.models import Session
from typing import Optional
from collections.abc import Sequence

class SessionRepository:
    """Репозиторий для работы с сессиями"""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def add_session(self, user_id: int, token: str, ip: str, user_agent: str, created_at: datetime) -> Session:
        """Добавление сессии"""
        session = Session(
            user_id=user_id,
            token=token,
            ip=ip,
            user_agent=user_agent,
            created_at=created_at,
        )
        self.db_session.add(session)
        await self.db_session.flush()
        return session
    
    async def get_user_sessions(self, user_id: int) -> Sequence[Session]:
        """Возвращает все сессии пользователя"""
        result = await self.db_session.execute(select(Session).where(Session.user_id == user_id))
        return result.scalars().all()
    
    async def get_session_by_token(self, access_token: str) -> Optional[Session]:
        """Находит сессию по токену"""
        result = await self.db_session.execute(select(Session).where(Session.token == access_token))
        return result.scalar_one_or_none()

    async def get_session_by_id(self, session_id: int) -> Optional[Session]:
        """Находит сессию по ID"""
        result = await self.db_session.execute(select(Session).where(Session.id == session_id))
        return result.scalar_one_or_none()
    
    async def delete_session(self, session_id: int) -> None:
        """Удаляет сессию по ID"""
        await self.db_session.execute(delete(Session).where(Session.id == session_id))
    