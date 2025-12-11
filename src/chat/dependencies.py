from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.chat.facade import ChatFacade
from src.message.dependencies import get_message_service
from src.dependencies import get_db_session
from src.chat.repository import ChatRepository
from src.chat.service import ChatService
from src.user.dependencies import get_user_service
from src.websocket.dependencies import get_websocket_manager
from src.websocket.manager import WebSocketManager

def get_chat_repository(session: AsyncSession = Depends(get_db_session)) -> ChatRepository:
    return ChatRepository(session)

def get_chat_service(
    chat_repo: ChatRepository = Depends(get_chat_repository),
) -> ChatService:
    return ChatService(chat_repository=chat_repo)

def get_chat_facade(
    db_session: AsyncSession = Depends(get_db_session),
    chat_service=Depends(get_chat_service),
    message_service=Depends(get_message_service),
    user_service=Depends(get_user_service),
    ws_manager: WebSocketManager = Depends(get_websocket_manager),
) -> ChatFacade:
    return ChatFacade(
        db_session=db_session,
        chat_service=chat_service,
        message_service=message_service,
        user_service=user_service,
        ws_manager=ws_manager,
    )