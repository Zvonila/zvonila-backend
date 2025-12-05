from src.database import async_session
from functools import wraps
from sqlalchemy.ext.asyncio import AsyncSession

async def get_db_session():
    async with async_session() as session:
        yield session

def transactional(func):
    """
    Умный декоратор, поддерживающий вложенные транзакции:
    - Если уже есть активная транзакция → не открывает новую;
    - При ошибке во внутренней транзакции вызывает rollback и пробрасывает исключение, это приводит к откату всей внешней транзакции.
    """
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        session: AsyncSession | None = getattr(self, "db_session", None)
        if session is None:
            raise RuntimeError(
                f"{self.__class__.__name__}.{func.__name__} требует self.db_session (AsyncSession)"
            )

        # Если уже в транзакции
        if session.in_transaction() or session.in_nested_transaction():
            try:
                return await func(self, *args, **kwargs)
            except Exception as e:
                if session.in_transaction():
                    await session.rollback()
                raise e

        # Если транзакции нет — открываем новую
        try:
            async with session.begin():
                return await func(self, *args, **kwargs)
        except Exception as e:
            if session.in_transaction():
                await session.rollback()
            raise e

    return wrapper