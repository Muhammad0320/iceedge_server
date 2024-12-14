from fastapi import APIRouter, Depends, status, HTTPException, Body, Query, Path
from sqlalchemy import select, update
from ..db.model import Category, Product
from ..db.schema import ProductCreate, ProductRead, ProductUpdate, Message, Cat
from datetime import datetime
from ..db.db_conn import AsyncSession, get_async_session
from typing import Sequence

router = APIRouter(prefix='/products', tags=['products'])

async def  get_category_by_name(name: Cat, session: AsyncSession = Depends(get_async_session)) -> Category: 
    query = select(Category).where(Category.name == name)
    return (await session.execute(query)).scalar_one() 

async def get_prods_by_cat(cat: Cat, session: AsyncSession = Depends(get_async_session)) -> Sequence[Product]: 
    cat_id = (await get_category_by_name(cat)).id 
    q = select(Product).where(Product.cat_id == cat_id).order_by(Product.name)
    return (await session.scalars(q)).all() 

async def check_product_or_404(id: int, session: AsyncSession = Depends(get_async_session)) -> Product : 
    q = select(Product).where(Product.id == id)
    res = (await session.execute(q)).scalar_one_or_none() 
    if not res: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found") 
    return res
    
async def get_products(skip: int = Query(0), limit: int = Query(None, max=100, min=1), session: AsyncSession = Depends(get_async_session)):
    q = select(Product).order_by(Product.created_at).offset(skip).limit(limit)
    return (await session.scalars(q)).all() 

@router.post('/', status_code=status.HTTP_201_CREATED,  response_model=ProductRead,responses={ status.HTTP_409_CONFLICT: {"model": Message()} }, 
)
async def add_new_prod( new_product: ProductCreate =  Body(example=ProductCreate(name="Product name", price=9999.99,description="product description" ,discount=10, cat=Cat.SHIIRT, thumbnail='product_thumbnail.jpg', amt_left=5, gallery=['second_img.jpg', 'first_img.jpg'], created_at=datetime.now() )), session: AsyncSession = Depends(get_async_session)): 
    fetched_cat = await get_category_by_name(new_product.cat) 
    product = Product(**new_product.model_dump(exclude_unset=True))
    product.cat_id = fetched_cat.id 
    session.add(product) 
    await session.commit()   
    return product

@router.get('/', response_model=list[ProductRead])
async def get_all_products(): 
    products = await get_products()
    return products

@router.get('/{cat}')
async def get_products_by_category(cat: Cat = Query(example=Cat.SHIIRT)): 
    products = await get_prods_by_cat(cat=cat)
    return products

@router.patch('/{id}')