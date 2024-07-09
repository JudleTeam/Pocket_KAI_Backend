from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config import get_settings


settings = get_settings()
engine = create_async_engine(settings.database_url)
AsyncSessionmaker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session():
    async with AsyncSessionmaker() as session:
        yield session
