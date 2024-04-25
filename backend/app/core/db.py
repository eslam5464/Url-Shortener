from collections.abc import AsyncGenerator

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings

engine = create_async_engine(settings.db_url.human_repr(), echo=settings.db_echo, future=True)
meta = MetaData(schema=settings.db_schema)


async def get_session() -> AsyncGenerator:
    async_session_factory = async_sessionmaker(
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
        bind=engine,
        class_=AsyncSession,
    )

    async with async_session_factory() as session:
        yield session
