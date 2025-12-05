from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update
from src.user.models import User
from typing import Optional
from collections.abc import Sequence

class UserRepository:
    """Репозиторий для работы с таблицей пользователей"""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def find_user_by_email(self, email: str) -> Optional[User]:
        """Поиск пользователя по email"""
        result = await self.db_session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def find_user_by_id(self, id: int) -> Optional[User]:
        """Поиск пользователя по id"""
        result = await self.db_session.execute(select(User).where(User.id == id))
        return result.scalar_one_or_none()
    
    async def get_users(self) -> Sequence[User]:
        """Получение всех пользователей"""
        result = await self.db_session.execute(select(User))
        return result.scalars().all()

    async def add_user(self, email: str, name: str, hash_password: str) -> Optional[User]:
        """Создание пользователя"""
        stmt = insert(User).values(email=email, name=name, password=hash_password).returning(User)
        result = await self.db_session.execute(stmt)
        return result.scalar_one()

    async def update_user(self, id: int, hash_password: Optional[str] = None, name: Optional[str] = None) -> None | User:
        """Обновление параметров пользователя, если параметр не None"""
        update_data = {}
        if hash_password: 
            update_data['password'] = hash_password
        if name: 
            update_data['name'] = name

        if not update_data:
            return None

        stmt = update(User).where(User.id == id).values(**update_data).returning(User)
        result = await self.db_session.execute(stmt)
        return result.scalar_one_or_none()