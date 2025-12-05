from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from src.config import settings

conn_str = (
    "postgresql+psycopg://"
    f"{settings.POSTGRESQL_USERNAME}:{settings.POSTGRESQL_PASSWORD}"
    f"@{settings.POSTGRESQL_HOST}:{settings.POSTGRESQL_PORT}"
    f"/{settings.POSTGRESQL_DB_NAME}"
)

engine = create_async_engine(conn_str, echo=False)

async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)