from sqlalchemy.ext.asyncio import AsyncSession
from src.message.repository import MessageRepository
from src.message.service import MessageService
from src.chat.service import ChatService
from src.user.service import UserService
from src.dependencies import get_db_session
from fastapi import Depends
from src.chat.dependencies import get_chat_service
from src.user.dependencies import get_user_service
from src.websocket.manager import WebSocketManager
from src.websocket.dependencies import get_websoket_manager

def get_message_repository(db_session: AsyncSession = Depends(get_db_session)) -> MessageRepository:
    """Фабрика для создания репозитория сообщений"""
    return MessageRepository(db_session)

def get_message_service(
    db_session: AsyncSession = Depends(get_db_session),
    message_repo: MessageRepository = Depends(get_message_repository),
    chat_service: ChatService = Depends(get_chat_service),
    user_service: UserService = Depends(get_user_service),
    ws_manager: WebSocketManager = Depends(get_websoket_manager)
) -> MessageService:
    """Фабрика для создания сервиса сообщений"""
    return MessageService(
        message_repo=message_repo,
        db_session=db_session,
        chat_service=chat_service,
        user_service=user_service,
        ws_manager=ws_manager,
    )