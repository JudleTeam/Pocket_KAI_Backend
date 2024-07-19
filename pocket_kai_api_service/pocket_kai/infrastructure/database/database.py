from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from pocket_kai.config import PostgresSettings


def new_session_maker(
    postgres_settings: PostgresSettings,
) -> async_sessionmaker[AsyncSession]:
    engine = create_async_engine(
        postgres_settings.database_uri,
        pool_size=15,
        max_overflow=15,
    )

    return async_sessionmaker(
        engine,
        class_=AsyncSession,
        autoflush=False,
        expire_on_commit=False,
    )
