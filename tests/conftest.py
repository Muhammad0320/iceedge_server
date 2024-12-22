from fastapi import status 
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
import pytest_asyncio
from ..main import app
from ..db.db_conn import get_async_session
from ..db.model import Base
import pytest

TEST_DB_URL='sqlite+aiosqlite:///:memory:'
test_engine = create_async_engine(TEST_DB_URL, echo=True) 
async_session = async_sessionmaker(bind=test_engine, expire_on_commit=False) 

async def get_test_session(): 
    async with async_session() as session: 
        yield session


@pytest_asyncio.fixture(scope='module', autouse=True) 
async def prepare_db(): 
    async with test_engine.begin() as conn: 
        await conn.run_sync(Base.metadata.create_all) 
    yield
    async with test_engine.begin() as conn: 
        await conn.run_sync(Base.metadata.drop_all) 

@pytest_asyncio.fixture(scope='module')
async def test_client():
    app.dependency_overrides[get_async_session] = get_test_session
    async with TestClient(app=app) as c: 
        yield c 

