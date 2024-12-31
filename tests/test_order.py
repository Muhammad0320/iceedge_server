import pytest
import pytest_asyncio
import httpx
from fastapi import status, HTTPException
from .conftest import TestUser, Role
from ..main import app
from ..db.db_conn import get_async_session
from ..db.model import User 
from ..db.schema import UserCreate, UserUpdate, OrderCreate, OrderRead
from ..routers.product import get_curr_user, Product, Cat
from uuid import uuid4

class TestGetOneOrder: 
    def __init__(self): 
        self.url = '/orders/'

    async def test_get_all(self, test_client: httpx.AsyncClient): 
        result = await test_client.get(self.url)
        assert result.status_code == status.HTTP_401_UNAUTHORIZED
    
    async def test_verboten(self, test_client: httpx.AsyncClient): 
        app.dependency_overrides[get_curr_user] = TestUser(Role.CUSTOMER).get_fake_user
        result = await test_client.get(self.url) 
        assert result.status_code == status.HTTP_403_FORBIDDEN
    
    