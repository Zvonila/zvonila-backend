from sqlalchemy.ext.asyncio import AsyncSession
from src.message.models import Message
from sqlalchemy import insert, select, delete
from collections.abc import Sequence
from typing import Optional

class MessageRepository:
    """Репозиторий для работы с сообщениями"""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_message(self, chat_id: int, sender_id: int, text: str):
        """Создание нового сообщения"""
        stmt = (
            insert(Message)
            .values(
                chat_id=chat_id,
                sender_id=sender_id,
                text=text
            )
            .returning(Message)
        )

        result = await self.db_session.execute(stmt)
        await self.db_session.commit()

        return result.scalar_one()
    
    async def find_message_by_id(self, message_id: int) -> Optional[Message]:
        """Поиск сообщения по id"""
        result = await self.db_session.execute(
            select(Message).where(Message.id == message_id)
        )
        return result.scalar_one_or_none()
    
    async def list_messages(self, chat_id: int, limit: int = 100, offset: int = 0) -> Sequence[Message]:
        """Получение списка сообщений в чате"""
        result = await self.db_session.execute(
            select(Message)
            .where(Message.chat_id == chat_id)
            .limit(limit)
            .offset(offset)
        )
        return result.scalars().all()
    
    async def delete_message(self, message_id: int) -> None:
        """Удаление сообщения по id"""
        await self.db_session.execute(
            delete(Message).where(Message.id == message_id)
        )
        await self.db_session.commit()  