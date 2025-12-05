from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from src.chat.models import Chat
from typing import Optional
from collections.abc import Sequence

class ChatRepository:
    """Репозиторий для работы с таблицей чатов"""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def find_chat_by_id(self, chat_id: int) -> Optional[Chat]:
        """Поиск чата по id"""
        result = await self.db_session.execute(
            select(Chat).where(Chat.id == chat_id)
        )
        return result.scalar_one_or_none()

    async def create_chat(self, initiator_id: int, receiver_id: int) -> Chat:
        """Создание нового чата"""
        stmt = (
            insert(Chat)
            .values(
                initiator_id=initiator_id,
                receiver_id=receiver_id
            )
            .returning(Chat)
        )

        result = await self.db_session.execute(stmt)
        await self.db_session.commit()

        return result.scalar_one()

    async def list_chats(self, user_id: int, limit: int = 100, offset: int = 0) -> Sequence[Chat]:
        """Получение списка чатов пользователя"""
        result = await self.db_session.execute(
            select(Chat)
            .where((Chat.initiator_id == user_id) | (Chat.receiver_id == user_id))
            .limit(limit)
            .offset(offset)
        )
        return result.scalars().all()

    async def delete_chat(self, chat_id: int) -> None:
        """Удаление чата по id"""
        await self.db_session.execute(
            delete(Chat).where(Chat.id == chat_id)
        )
        await self.db_session.commit()
