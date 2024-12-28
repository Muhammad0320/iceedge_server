import pytest
import pytest_asyncio
import httpx
from fastapi import status, HTTPException
from .conftest import TestUser, Role
from ..main import app
from ..db.db_conn import get_async_session
from ..routers.product import get_curr_user, Product, Cat


async def create_new_prod(test_client: httpx.AsyncClient, cat: Cat = Cat.SHIRT, name: str = 'Black Hoodie') -> Product: 
        new_prod = {
            'name':name, 'price':9999, 'discount':5, 'thumbnail':'thumbnail.png', 'gallery':['gallery_img_1.png', 'gallery_img_2.png'], 'amt_left':10, 'cat':cat, 'description':'Beautiful Hoodie'
        } 
        product = await test_client.post('/products/', json=new_prod) 
        assert product.status_code == status.HTTP_201_CREATED
        data: Product | None = product.json() 
        if not data: 
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        return data


@pytest_asyncio.fixture(scope='module', autouse=True)
async def create_test_product(test_client: httpx.AsyncClient): 
    return (await create_new_prod(test_client))
    
    
class TestCreateReview: 
    def __init__(self): 
        self.url = '/reviews/'
    
    async def test_unauthenticated(self, test_client: httpx.AsyncClient, product: Product): 
        payload = {"content": "Tested and trusted", "rating": 5.0,  'product_id': product.id   }
        result = await test_client.post(self.url, json=payload)
        assert result.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_purchase_prod(self, test_client: httpx.AsyncClient, product: Product): 
        app.dependency_overrides[get_curr_user] = TestUser(Role.CUSTOMER).get_fake_user
        payload = {"content": "Tested and trusted", "rating": 5.0,  'product_id': product.id   }
        result = await test_client.post(self.url, json=payload)
        assert result.status_code == status.HTTP_400_BAD_REQUEST
    
    async def test_invalid_fields(self, test_client: httpx.AsyncClient, product: Product): 
        app.dependency_overrides[get_curr_user] = TestUser(Role.CUSTOMER).get_fake_user
        payload = {"content": "Tested and trusted",  'product_id': product.id   }
        result = await test_client.post(self.url, json=payload)
        assert result.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    async def test_multiple_reviews(self, test_client: httpx.AsyncClient, product: Product):
        app.dependency_overrides[get_curr_user] = TestUser(Role.CUSTOMER).get_fake_user 
        payload = {"content": "Tested and trusted", "rating": 5.0,  'product_id': product.id   }
        result = await test_client.post(self.url, json=payload)
        result.status_code == status.HTTP_201_CREATED
        result2 = await test_client.post(self.url, json=payload) 
        result2.status_code == status.HTTP_409_CONFLICT
    
