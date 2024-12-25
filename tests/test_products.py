import pytest
import pytest_asyncio
import httpx
from fastapi import status, HTTPException
from .conftest import TestUser, Role
from ..main import app
from ..routers.product import get_curr_user, Product, Cat


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
        app.dependency_overrides[get_curr_user] = TestUser(Role.DEVELOPER).get_fake_user
        new_prod = {'name':'Black Hoodie', 'price':9999, 'discount':5, 'thumbnail':'thumbnail.png', 'gallery':['gallery_img_1.png', 'gallery_img_2.png'], 'amt_left':10, 'cat':Cat.SHIRT}
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
 
@pytest.mark.asyncio   
class TestGetProduct:
    async def test_get_product_invalid_format(self, test_client: httpx.AsyncClient): 
        res = await test_client.get('/prorducts/shit_password')
        assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    async def test_get_product_invalid_id(self, test_client: httpx.AsyncClient): 
        res = await test_client.get('/products/12')
        res.status_code == status.HTTP_404_NOT_FOUND
    
    async def test_get_product(self, test_client: httpx.AsyncClient): 
        app.dependency_overrides[get_curr_user] = TestUser(Role.DEVELOPER).get_fake_user
        new_prod = {
            'name':'Black Hoodie', 'price':9999, 'discount':5, 'thumbnail':'thumbnail.png', 'gallery':['gallery_img_1.png', 'gallery_img_2.png'], 'amt_left':10, 'cat':Cat.SHIRT, 'description':'Beautiful Hoodie'
        } 
        product = await test_client.post('/products/', json=new_prod) 
        assert product.status_code == status.HTTP_201_CREATED
        data: Product | None = product.json() 
        if not data: 
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        res = await test_client.get(f'/products/{data.id}')
        res.status_code == status.HTTP_200_OK
            
    
