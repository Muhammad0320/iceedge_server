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