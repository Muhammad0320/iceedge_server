from fastapi import status, Depends
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
import pytest_asyncio
from ..main import app
from ..db.db_conn import get_async_session
from ..db.model import Base, User
from ..db.schema import Role
import pytest

TEST_DB_URL='sqlite+aiosqlite:///:memory:'
test_engine = create_async_engine(TEST_DB_URL, echo=True) 
async_session = async_sessionmaker(bind=test_engine, expire_on_commit=False) 

async def get_test_session(): 
    async with async_session() as session: 
        yield session

async def get_fake_user_by_role(role: Role = Role.CUSTOMER):
    async def get_fake_user(session: AsyncSession = Depends(get_test_session)): 
        user = User(firstname="Muhammad", lastname='lastname', role=role, email='lisanalgaib@gmail.com', password='password1234')
        session.add(user) 
        await session.commit() 
        return user 
    return get_fake_user

class TestUser(): 
    def __init__(self, role: Role = Role.CUSTOMER): 
       self.role = role 
       
    async def get_fake_user(self, session: AsyncSession = Depends(get_test_session)): 
        user = User(firstname="Muhammad", lastname='lastname', role=self.role, email='lisanalgaib@gmail.com', password='password1234')
        session.add(user) 
        await session.commit() 
        return user 
    

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