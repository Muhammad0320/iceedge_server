import pytest
import pytest_asyncio
import httpx
from fastapi import status, HTTPException
from .conftest import TestUser, Role
from ..main import app
from ..routers.product import get_curr_user, Product, Cat


async def create_new_prod(test_client: httpx.AsyncClient, cat: Cat = Cat.SHIRT, name: str = 'Black Hoodie'): 
        new_prod = {
            'name':name, 'price':9999, 'discount':5, 'thumbnail':'thumbnail.png', 'gallery':['gallery_img_1.png', 'gallery_img_2.png'], 'amt_left':10, 'cat':cat, 'description':'Beautiful Hoodie'
        } 
        product = await test_client.post('/products/', json=new_prod) 
        assert product.status_code == status.HTTP_201_CREATED
        data: Product | None = product.json() 
        if not data: 
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        return data, new_prod

