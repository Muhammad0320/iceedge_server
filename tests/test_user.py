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
        self.url: str = '/users/register/'
        self.payload:  UserCreate = UserCreate(firstname="Muhammad", lastname='lastname', role=Role.CUSTOMER, email='lisanalgaib@gmail.com', password='password1234', password_confirm='password1234', address='G50, Balogun Gambari')
        
    
    async def test_invalid_fields(self, test_client: httpx.AsyncClient): 
        result = await test_client.post(self.url, json=self.payload.model_dump_json(exclude={'email'}))
        result.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    