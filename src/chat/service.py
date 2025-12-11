from src.chat.repository import ChatRepository
from sqlalchemy.ext.asyncio import AsyncSession
from src.dependencies import transactional
from src.chat.schemas import ChatSchema
from collections.abc import Sequence
from typing import cast, Optional
from src.websocket.manager import WebSocketManager

class ChatService:
    """Сервис для управления пользовательскими чатами"""

    def __init__(self, chat_repository: ChatRepository ):
        self.chat_repository = chat_repository


    async def create_chat(self, user_id: int, receiver_id: int) -> ChatSchema:
        """Создание нового чата"""
        if user_id == receiver_id:
            raise ValueError("Нельзя создать чат с самим собой")

        finded_chat = await self.chat_repository.find_chat_by_two_user(user_id, receiver_id)
        print(finded_chat)
        if finded_chat:
            raise ValueError("Чат уже существует")

        chat_obj = await self.chat_repository.create_chat(
            initiator_id=user_id, 
            receiver_id=receiver_id
        )

        return ChatSchema.model_validate(chat_obj)
    

    async def get_chat_by_id(self, chat_id: int, user_id: int) -> Optional[ChatSchema]:
        """Поиск чата по id"""
        chat = await self.chat_repository.find_chat_by_id(chat_id)
        if chat is None:
            return None

        initiator_id = cast(int, chat.initiator_id)
        receiver_id = cast(int, chat.receiver_id)

        if initiator_id == user_id or receiver_id == user_id:
            return ChatSchema.model_validate(chat)
        
        return None
    

    async def list_chats(self, user_id: int, limit: int = 100, offset: int = 0) -> Sequence[ChatSchema]:
        """Получение списка чатов пользователя"""
        chat_list = await self.chat_repository.list_chats(user_id, limit, offset)
        return [ChatSchema.model_validate(chat) for chat in chat_list]
    

    async def delete_chat(self, chat_id: int) -> None:
        """Удаление чата"""
        return await self.chat_repository.delete_chat(chat_id)