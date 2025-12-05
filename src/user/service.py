from src.user.repository import UserRepository
from src.user.exceptions import UserNotFoundError
from src.auth.exceptions import InvalidPasswordError
from src.auth.utils import PasswordService
from src.dependencies import transactional
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.schemas import UserSchema
from typing import cast, Optional
from collections.abc import Sequence

class UserService:
    """Сервис для управления пользователями"""

    def __init__(self, db_session: AsyncSession, user_repo: UserRepository, password_service: PasswordService):
        self.user_repo = user_repo
        self.password_service = password_service
        self.db_session = db_session

    @transactional
    async def change_password(self, user_id: int, password: str, new_password: str) -> None:
        """Изменяет пароль пользователя. Проверяет текущий пароль и обновляет его на новый"""
        user = await self.user_repo.find_user_by_id(id=user_id)
        if not user:
            raise UserNotFoundError()
        
        hash_password = cast(str, user.password)
        if not self.password_service.verify(
            hash_password=hash_password, 
            raw_password=password
        ):
            raise InvalidPasswordError()
        
        new_hash_password = self.password_service.hash(raw_password=new_password)
        
        await self.user_repo.update_user(
            id=user_id,
            hash_password=new_hash_password,
            name=None,
        )

    @transactional
    async def change_name(self, user_id, name: str) -> None:
        """Изменяет имя пользователя"""
        user = await self.user_repo.find_user_by_id(id=user_id)
        if not user:
            raise UserNotFoundError()
        
        await self.user_repo.update_user(
            id=user_id,
            hash_password=None,
            name=name,
        )

    @transactional
    async def get_user_by_id(self, user_id: int) -> Optional[UserSchema]:
        """Получение пользователя по id"""
        user_obj = await self.user_repo.find_user_by_id(id=user_id)
        if user_obj is None:
            return None
        
        return UserSchema.model_validate(user_obj)
    
    @transactional
    async def get_users(self) -> Sequence[UserSchema]:
        """Получение всех пользователей"""
        return [UserSchema.model_validate(user) for user in await self.user_repo.get_users()]