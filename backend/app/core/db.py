from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


TEST = settings.test

DATABASE_URL = settings.test_database_url if TEST else settings.database_url

engine = create_async_engine(DATABASE_URL, echo=False, future=True)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# engine = create_async_engine(DATABASE_URL, echo=False, future=True)
# async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_async_session():
    async with AsyncSessionLocal() as async_session:
        yield async_session


# async def get_async_session():
#     async with async_session_maker() as async_session:
#         yield async_session
