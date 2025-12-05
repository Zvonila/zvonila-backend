from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.dependencies import get_db_session
from src.chat.repository import ChatRepository
from src.chat.service import ChatService
from src.user.dependencies import get_user_service

def get_chat_repository(session: AsyncSession = Depends(get_db_session)) -> ChatRepository:
    return ChatRepository(session)

def get_chat_service(
    db_session: AsyncSession = Depends(get_db_session),
    chat_repo: ChatRepository = Depends(get_chat_repository),
    user_service = Depends(get_user_service)
) -> ChatService:
    return ChatService(chat_repo, db_session, user_service)