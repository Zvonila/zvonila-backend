from sqlalchemy.ext.asyncio import AsyncSession
from src.user.service import UserService
from src.chat.service import ChatService
from src.message.repository import MessageRepository
from typing import Optional, cast
from collections.abc import Sequence
from src.message.schemas import MessageSchema
from src.websocket.manager import WebSocketManager

class MessageService:
    """Сервис для работы с сообщениями"""

    def __init__(
            self, 
            message_repo: MessageRepository, 
            db_session: AsyncSession, 
            chat_service: ChatService, 
            user_service: UserService,
            ws_manager: WebSocketManager
        ):
        self.message_repo = message_repo
        self.db_session = db_session
        self.chat_service = chat_service
        self.user_service = user_service
        self.ws_manager = ws_manager

    async def send_message(self, chat_id: int, sender_id: int, text: str) -> MessageSchema:
        """Отправка сообщения в чат"""
        chat = await self.chat_service.get_chat_by_id(chat_id, sender_id)
        if chat is None:
            raise ValueError("Чат не найден или пользователь не имеет доступа")

        if await self.user_service.get_user_by_id(sender_id) is None:
            raise ValueError("Пользователь-отправитель не найден")

        message_obj = await self.message_repo.create_message(chat_id=chat_id, sender_id=sender_id, text=text)

        await self.ws_manager.send(chat.receiver_id, "message", MessageSchema.model_validate(message_obj).model_dump_json())

        return MessageSchema.model_validate(message_obj)
    

    async def get_message(self, message_id: int, user_id: int) -> Optional[MessageSchema]:
        """Получение сообщения по id"""
        message = await self.message_repo.find_message_by_id(message_id)
        if message is None:
            return None

        chat_id = cast(int, message.chat_id)
        chat = await self.chat_service.get_chat_by_id(chat_id, user_id)
        if chat is None:
            return None

        return MessageSchema.model_validate(message)
    

    async def list_messages(self, chat_id: int, user_id: int, limit: int = 100, offset: int = 0) -> Sequence[MessageSchema]:
        """Получение списка сообщений в чате"""
        chat = await self.chat_service.get_chat_by_id(chat_id, user_id)
        if chat is None:
            raise ValueError("Чат не найден или пользователь не имеет доступа")

        return [MessageSchema.model_validate(msg) for msg in await self.message_repo.list_messages(chat_id, limit, offset)]
    
    async def delete_message(self, message_id: int, user_id: int) -> None:
        """Удаление сообщения по id"""
        message = await self.message_repo.find_message_by_id(message_id)
        if message is None:
            raise ValueError("Сообщение не найдено")

        chat_id = cast(int, message.chat_id)
        chat = await self.chat_service.get_chat_by_id(chat_id, user_id)
        if chat is None:
            raise ValueError("Чат не найден или пользователь не имеет доступа")

        await self.message_repo.delete_message(message_id)