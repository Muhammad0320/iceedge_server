import pytest
import pytest_asyncio
import httpx
from fastapi import status
from .conftest import TestUser, Role
from ..main import app
from ..routers.product import get_curr_user, Product ,ProductCreate, Cat



@pytest.mark.asyncio 
class TestCreateProduct: 
    
    async def test_create_unauthorized(self, test_client: httpx.AsyncClient): 
        new_prod = {"name":'Black Hoodie', "price":9999, "discount":5, "thumbnail":'thumbnail.png', "gallery":['gallery_img_1.png', 'gallery_img_2.png'], "amt_left":10, "cat":Cat.SHIRT }
        res = await test_client.post('/products/', json=new_prod) 
        assert res.status_code == status.HTTP_401_UNAUTHORIZED
    
    async def test_create_forbidden(self, test_client: httpx.AsyncClient): 
        app.dependency_overrides[get_curr_user] = TestUser(Role.CUSTOMER).get_fake_user
        new_prod = {"name":'Black Hoodie', "price":9999, "discount":5, "thumbnail":'thumbnail.png', "gallery":['gallery_img_1.png', 'gallery_img_2.png'], "amt_left":10, "cat":Cat.SHIRT, "description":'Beatiful  Hoodie' }
        res = await test_client.post('/products/', json=new_prod) 
        assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    async def test_create_invalid_fields(self, test_client: httpx.AsyncClient): 
        app.dependency_overrides[get_curr_user] = get_fake_user_by_role(Role.DEVELOPER)
        new_prod = ProductCreate(name='Black Hoodie', price=9999, discount=5, thumbnail='thumbnail.png', gallery=['gallery_img_1.png', 'gallery_img_2.png'], amt_left=10, cat=Cat.SHIRT )
        res = await test_client.post('/products/', json=new_prod) 
        assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    async def test_create_valid(self, test_client: httpx.AsyncClient): 
        app.dependency_overrides[get_curr_user] = TestUser(Role.DEVELOPER).get_fake_user
        new_prod = {
            'name':'Black Hoodie', 'price':9999, 'discount':5, 'thumbnail':'thumbnail.png', 'gallery':['gallery_img_1.png', 'gallery_img_2.png'], 'amt_left':10, 'cat':Cat.SHIRT, 'description':'Beautiful Hoodie'
        } 
        res = await test_client.post('/products/', json=new_prod) 
        assert res.status_code == status.HTTP_201_CREATED
        data: Product | None = res.json() 
        if data: 
            assert data.name == new_prod['name']
        