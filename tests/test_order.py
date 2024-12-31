import pytest
import pytest_asyncio
import httpx
from fastapi import status, HTTPException
from .conftest import TestUser, Role
from ..main import app
from ..db.db_conn import get_async_session
from ..db.model import Order, OrderItem
from ..db.schema import UserCreate, UserUpdate, OrderCreate, OrderRead
from ..routers.product import get_curr_user, Product, Cat
from uuid import uuid4
from .test_reviews import create_new_prod

class TestGetOrders: 
    def __init__(self): 
        self.url = '/orders/'

    async def test_get_all(self, test_client: httpx.AsyncClient): 
        result = await test_client.get(self.url)
        assert result.status_code == status.HTTP_401_UNAUTHORIZED
    
    async def test_verboten(self, test_client: httpx.AsyncClient): 
        app.dependency_overrides[get_curr_user] = TestUser(Role.CUSTOMER).get_fake_user
        result = await test_client.get(self.url) 
        assert result.status_code == status.HTTP_403_FORBIDDEN
    
    async def test_valid(self, test_client: httpx.AsyncClient): 
        app.dependency_overrides[get_curr_user] = TestUser(Role.DEVELOPER).get_fake_user
        result = await test_client.get(self.url) 
        assert result.status_code == status.HTTP_200_OK
        
@pytest_asyncio.fixture(scope='module', autouse=True)
async def create_test_product(test_client: httpx.AsyncClient): 
    return (await create_new_prod(test_client))

customer_id=uuid4()    

@pytest_asyncio.fixture(scope='module')
async def create_test_order(product: Product ,test_client: httpx.AsyncClient) -> Order: 
    app.dependency_overrides[get_curr_user] = TestUser(Role.DEVELOPER, customer_id).get_fake_user
    order = Order(total=500, quantity=10, shipping_fee=50, shipping_address='G50', customer_id=customer_id, order_item=['Order_item'])
    Order_item = OrderItem(unit_price=100, quantity=5, product_id=product.id, order_id=order.id)
    await test_client.post('/order', json=order)
    return order

class TestGetOneOrder:
    def __init__(self):
        self.url = '/orders/'
    
    async def test_unauthorized(self, test_client: httpx.AsyncClient): 
        result = await test_client.get(f"{self.url}/1234")
        assert result.status_code == status.HTTP_401_UNAUTHORIZED
    
    async def test_not_found(self, test_client: httpx.AsyncClient): 
        app.dependency_overrides[get_curr_user] = TestUser(Role.CUSTOMER).get_fake_user
        result = await test_client.get(self.url)
        assert result.status_code == status.HTTP_404_NOT_FOUND
    
    async def test_valid(self, test_client: httpx.AsyncClient, order: Order): 
        app.dependency_overrides[get_curr_user] = TestUser(Role.CUSTOMER).get_fake_user
        result = await test_client.get(f"{self.url}{order.id}")
        assert result.status_code == status.HTTP_200_OK
    

class TestGetMyOrder: 
    def __init__(self): 
        self.url = '/orders/my_orders'
    
    async def test_unauthorized(self, test_client: httpx.AsyncClient): 
        result = await test_client.get(self.url)
        assert result.status_code ==status.HTTP_401_UNAUTHORIZED
    
    async def test_not_found(self, test_client: httpx.AsyncClient): 
        app.dependency_overrides[get_curr_user] = TestUser(Role.CUSTOMER).get_fake_user
        result = await test_client.get(self.url)
        assert result.status_code == status.HTTP_403_FORBIDDEN
    
    