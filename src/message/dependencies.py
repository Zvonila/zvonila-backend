from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.message.repository import MessageRepository
from src.message.service import MessageService
from src.dependencies import get_db_session

def get_message_repository(db_session: AsyncSession = Depends(get_db_session)) -> MessageRepository:
    """Фабрика для создания репозитория сообщений"""
    return MessageRepository(db_session)

def get_message_service(
    message_repo: MessageRepository = Depends(get_message_repository),
) -> MessageService:
    """Фабрика для создания сервиса сообщений"""
    return MessageService(
        message_repo=message_repo,
    )