import pytest
import pytest_asyncio
import httpx
from fastapi import status, HTTPException
from .conftest import TestUser, Role
from ..main import app
from ..db.db_conn import get_async_session
from ..db.model import Review
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
    
    async def test_create_review(self, test_client: httpx.AsyncClient, product: Product): 
        app.dependency_overrides[get_curr_user] = TestUser(Role.CUSTOMER).get_fake_user 
        payload = {"content": "Tested and trusted", "rating": 5.0,  'product_id': product.id   }
        result = await test_client.post(self.url, json=payload)
        result.status_code == status.HTTP_201_CREATED

@pytest_asyncio.fixture(scope='module')
async def create_test_review(test_client: httpx.AsyncClient, product: Product): 
    app.dependency_overrides[get_curr_user] = TestUser(Role.CUSTOMER).get_fake_user 
    payload = {"content": "Tested and trusted", "rating": 5.0,  'product_id': product.id   }
    result = await test_client.post('/reviews/', json=payload)  
    assert result.status_code == status.HTTP_201_CREATED
    review: Review | None = result.json() 
    if not review: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return review


class TestGetOneReview: 
    def __init__(self): 
        self.url = '/reviews/'
        
    async def test_get_one(self, test_client: httpx.AsyncClient, review: Review): 
        result = await test_client.get(f"{self.url}{review.id}")
        result.status_code == status.HTTP_200_OK

class TestUpdateReview: 
    def __init__(self): 
        self.url = '/reviews/'
    
    async def test_unauthorized(self, test_client: httpx.AsyncClient, review: Review):
        updates = {"rating": 4.5}
        result = await test_client.patch(f"{self.url}{review.id}", json=updates) 
        assert result.status_code == status.HTTP_401_UNAUTHORIZED
        
        