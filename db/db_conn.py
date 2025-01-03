from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession , create_async_engine, async_sessionmaker
from  .model import Base

DB_URL='sqlite+aiosqlite:///./iceedge.db'
engine = create_async_engine(DB_URL) 
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]: 
    async with async_session_maker() as session: 
        yield session


async def create_all_tables(): 
    async with engine.begin() as conn: 
        await conn.run_sync(Base.metadata.create_all)