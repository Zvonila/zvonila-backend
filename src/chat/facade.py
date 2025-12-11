

from collections.abc import Sequence
import json
from typing import List, Optional

from src.auth.schemas import UserSchema
from src.chat.schemas import ChatSchema, ChatWithDetails
from src.chat.service import ChatService
from src.message.schemas import MessageSchema
from src.message.service import MessageService
from src.user.service import UserService
from src.websocket.manager import WebSocketManager
from sqlalchemy.ext.asyncio import AsyncSession


class ChatFacade:
    def __init__(
            self,
            db_session: AsyncSession,
            chat_service: ChatService,
            message_service: MessageService,
            user_service: UserService,
            ws_manager: WebSocketManager
        ) -> None:
        self.db_session = db_session
        self.chat_service = chat_service
        self.message_service = message_service
        self.user_service = user_service
        self.ws_manager = ws_manager

    async def get_chats(self, user_id: int) -> List[ChatWithDetails]:
        detailed_chat_list: List[ChatWithDetails] = []

        chat_list = await self.chat_service.list_chats(user_id)

        for chat in chat_list:
            chat_user_id = chat.receiver_id if chat.initiator_id == user_id else chat.initiator_id
            last_message = await self._get_last_message(chat_id=chat.id)
            user = await self.user_service.get_user_by_id(user_id=chat_user_id)

            detailed_chat = ChatWithDetails(
                **ChatSchema.model_validate(chat).model_dump(),
                companion=UserSchema.model_validate(user),
                last_message = MessageSchema.model_validate(last_message) if last_message else None
            )

            detailed_chat_list.append(detailed_chat)

        return detailed_chat_list
    

    async def send_message(self, chat_id: int, sender_id: int, text: str) -> MessageSchema:
        chat = await self.chat_service.get_chat_by_id(chat_id, sender_id)
        if chat is None:
            raise ValueError("Чат не найден или пользователь не имеет доступа")

        if await self.user_service.get_user_by_id(sender_id) is None:
            raise ValueError("Пользователь-отправитель не найден")

        message_obj = await self.message_service.create(chat_id, sender_id, text)

        destination_id = chat.initiator_id if chat.receiver_id == sender_id else chat.receiver_id 

        await self.ws_manager.send(
            destination_id, 
            "message", 
            message_obj.model_dump_json()
        )

        return message_obj

    
    async def delete_chat(self, user_id: int, chat_id: int) -> None:
        chat = await self.chat_service.get_chat_by_id(chat_id, user_id)
        if not chat:
            raise ValueError("Чат не найден")

        await self.chat_service.delete_chat(chat_id)

        destination_id = chat.initiator_id if chat.receiver_id == user_id else chat.receiver_id 

        await self.ws_manager.send(
            destination_id,
            "deleted_chat", 
            json.dumps({ "chat_id": chat_id })
        )

    
    async def create_chat(self, user_id: int, receiver_id: int) -> ChatWithDetails:
        chat = await self.chat_service.create_chat(user_id, receiver_id)
        destination_id = chat.initiator_id if chat.receiver_id == user_id else chat.receiver_id 

        chat_user_id = chat.receiver_id if chat.initiator_id == user_id else chat.initiator_id
        user = await self.user_service.get_user_by_id(user_id=chat_user_id)

        detailed_chat = ChatWithDetails(
            **ChatSchema.model_validate(chat).model_dump(),
            companion=UserSchema.model_validate(user),
        )

        await self.ws_manager.send(
            destination_id, 
            "created_chat", 
            detailed_chat.model_dump_json()
        )

        return detailed_chat
    

    async def delete_message(self, message_id: int, user_id: int) -> None:
        message = await self.message_service.get(message_id)
        if message is None:
            raise ValueError("Сообщение не найдено")
        
        chat = await self.chat_service.get_chat_by_id(
            chat_id=message.chat_id, 
            user_id=user_id
        )
        if chat is None:
            raise ValueError("Чат не найден или пользователь не имеет доступа")
        
        await self.message_service.delete(message_id)

        destination_id = chat.initiator_id if chat.receiver_id == user_id else chat.receiver_id 

        await self.ws_manager.send(
            destination_id,
            "deleted_message", 
            json.dumps({ 
                "chat_id": chat.id,
                "message_id": message_id 
            })
        )


    async def get_messages(self, chat_id: int, user_id: int, limit: int = 100, offset: int = 0) -> Sequence[MessageSchema]: 
        chat = await self.chat_service.get_chat_by_id(chat_id, user_id)
        if chat is None:
            raise ValueError("Чат не найден или пользователь не имеет доступа")

        messages_list = await self.message_service.list_for_chat(chat_id, limit, offset) 

        return [MessageSchema.model_validate(msg) for msg in messages_list]
    
    
    async def _get_last_message(self, chat_id: int) -> Optional[MessageSchema]:
        messages = await self.message_service.list_for_chat(
                chat_id=chat_id,
                limit=1,
                offset=0
            )
        return messages[0] if messages else None