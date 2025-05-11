from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator
from config.settings import settings

# Создание асинхронного движка SQLAlchemy
engine = create_async_engine(
    url=settings.get_psql_async_connect_url(),
    echo=True,
)

# Фабрика асинхронных сессий
session_maker = async_sessionmaker(engine, expire_on_commit=False)

@asynccontextmanager
async def get_session_context() -> AsyncGenerator[AsyncSession, None]:
    """
    Асинхронный контекстный менеджер, создающий сессию SQLAlchemy на время выполнения запроса.
    Гарантирует закрытие сессии после использования.
    """
    async with session_maker() as session:
        yield session

async def get_async_session() -> AsyncSession:
    """
    Dependency-функция FastAPI для получения активной сессии БД.
    Использует контекстный менеджер для управления временем жизни сессии.
    """
    async with get_session_context() as session:
        return session




