from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.dependencies import get_db_session
from src.sessions.repository import SessionRepository
from src.sessions.service import SessionService

def get_session_repository(session: AsyncSession = Depends(get_db_session)) -> SessionRepository:
    return SessionRepository(session)

def get_session_service(
    db_session: AsyncSession = Depends(get_db_session),
    session_repo: SessionRepository = Depends(get_session_repository)
) -> SessionService:
    return SessionService(db_session, session_repo)
