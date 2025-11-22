from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from config.settings import settings
from typing import AsyncGenerator


class Base(DeclarativeBase):
    pass


engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)


async def get_session() -> AsyncGenerator:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
