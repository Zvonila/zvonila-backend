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

    def __init__(self, message_repo: MessageRepository):
        self.message_repo = message_repo


    async def create(self, chat_id: int, sender_id: int, text: str) -> MessageSchema:
        """Отправка сообщения в чат"""
        if not text.strip():
            raise ValueError("Текст сообщения не может быть пустым")
        
        message_obj = await self.message_repo.create_message(
            chat_id=chat_id,
            sender_id=sender_id,
            text=text
        )
        return MessageSchema.model_validate(message_obj)
    

    async def get(self, message_id: int) -> Optional[MessageSchema]:
        """ Получение сообщения по ID """
        message = await self.message_repo.find_message_by_id(message_id)
        if message is None:
            return None
        return MessageSchema.model_validate(message)


    async def list_for_chat(self, chat_id: int, limit: int = 100, offset: int = 0) -> Sequence[MessageSchema]:
        """ Получение списка сообщений для чата """
        messages = await self.message_repo.list_messages(chat_id, limit, offset)
        return [MessageSchema.model_validate(msg) for msg in messages]


    async def delete(self, message_id: int) -> None:
        """  Удаление сообщения по ID """
        message = await self.message_repo.find_message_by_id(message_id)
        if message is None:
            raise ValueError("Сообщение не найдено")
        await self.message_repo.delete_message(message_id)