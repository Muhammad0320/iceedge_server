import pytest
import pytest_asyncio
import httpx
from fastapi import status, HTTPException
from .conftest import TestUser, Role
from ..main import app
from ..db.db_conn import get_async_session
from ..db.model import User 
from ..db.schema import UserCreate, UserUpdate
from ..routers.product import get_curr_user, Product, Cat
from uuid import uuid4


class Register: 
    def __init__(self): 
        self.url = '/users/register/'
        self.payload = UserCreate(firstname="Muhammad", lastname='lastname', role=Role.CUSTOMER, email='lisanalgaib@gmail.com', password='password1234', password_confirm='password1234', address='G50, Balogun Gambari')
        
    
    async def test_invalid_fields(self, test_client: httpx.AsyncClient): 
        result = await test_client.post(self.url, json=self.payload.model_dump_json(exclude={'email'}))
        result.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    async def test_different_passwords(self, test_client: httpx.AsyncClient): 
        self.payload.password_confirm = 'pass12345'
        result = await test_client.post(self.url, json=self.payload.model_dump_json()) 
        result.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    async def test_multiple_resgistration(self, test_client: httpx.AsyncClient): 
        result = await test_client.post(self.url, json=self.payload.model_dump_json()) 
        result.status_code == status.HTTP_201_CREATED
        
        result = await test_client.post(self.url, json=self.payload.model_dump_json()) 
        result.status_code == status.HTTP_409_CONFLICT
    
    async def test_valid(self, test_client: httpx.AsyncClient): 
        result = await test_client.post(self.url, json=self.payload.model_dump_json()) 
        result .status_code == status.HTTP_201_CREATED

class Login: 
    def __init__(self): 
        self.url = '/users/login/'
        self.payload = {'email': "lisanalgaib@gmail.com", 'password': 'password1234'}
    
    async def test_non_existing_user(self, test_client: httpx.AsyncClient): 
        self.payload['email'] = 'balogun@gmail.com'
        result = await test_client.post(self.url, json=self.payload) 
        assert result.status_code == status.HTTP_401_UNAUTHORIZED
    
    async def test_invalid_credentials(self, test_client: httpx.AsyncClient): 
        self.payload['password'] = 'pass1234'
        result = await test_client.post(self.url, json=self.payload) 
        assert result.status_code == status.HTTP_401_UNAUTHORIZED  
    
    async def test_valid(self, test_client: httpx.AsyncClient): 
        result = await test_client.post(self.url, json=self.payload)
        assert result.status_code == status.HTTP_200_OK

class Me:
    def __init__(self):
        self.url = '/users/me'
    
    async def test_unauthenticated(self, test_client: httpx.AsyncClient): 
        result = await test_client.get(self.url)
        assert result.status_code == status.HTTP_401_UNAUTHORIZED
    
    async def test_valid(self, test_client: httpx.AsyncClient): 
        app.dependency_overrides[get_curr_user] = TestUser(Role.CUSTOMER).get_fake_user
        result = await test_client.get(self.url)        
        assert result.status_code == status.HTTP_200_OK
    