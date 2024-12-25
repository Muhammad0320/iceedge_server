from fastapi import APIRouter, Depends, status, HTTPException, Body, Query, Path
from sqlalchemy import select, update, delete, func
from sqlalchemy.orm import joinedload
from ..db.model import Category, Product, User 
from datetime import datetime
from ..dependencies import get_curr_user, Rbac
from ..db.db_conn import AsyncSession, get_async_session
from typing import Sequence
from ..db.schema import ProductCreate, ProductRead, ProductUpdate, Message, Cat, Role

router = APIRouter(prefix='/products', tags=['products'])

async def  get_category_by_name(name: Cat, session: AsyncSession = Depends(get_async_session)) -> Category: 
    query = select(Category).where(Category.name == name)
    return (await session.execute(query)).scalar_one() 


async def get_prods_by_cat(cat: Cat, session: AsyncSession = Depends(get_async_session)) -> Sequence[Product]: 
    cat_id = (await get_category_by_name(cat)).id 
    q = select(Product, Category.name).where(Product.cat_id == cat_id).join(Product.cat).order_by(Product.created_at).options(joinedload(Product.cat))
    return (await session.scalars(q)).all() 

async def get_product_or_404(id: int, session: AsyncSession = Depends(get_async_session)) -> Product : 
    q = select(Product, Category.name).where(Product.id == id).options(joinedload(Product.cat))
    res = (await session.execute(q)).scalar_one_or_none() 
    if not res: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found") 
    return res
    
async def get_products(skip: int = Query(0), limit: int = Query(None, max=100, min=1), session: AsyncSession = Depends(get_async_session)):
    q = select(Product).order_by(Product.created_at).offset(skip).limit(limit)
    return (await session.scalars(q)).all() 


@router.post('/', dependencies=[ Depends(get_curr_user), Depends(Rbac(role=[Role.DEVELOPER, Role.MERCHANT]).accessible_to)] ,status_code=status.HTTP_201_CREATED,  response_model=ProductRead,responses={ status.HTTP_409_CONFLICT: {"model": Message()} }, 
)
async def add_new_prod(new_product: ProductCreate =  Body(example=ProductCreate(name="Product name", price=9999.99,description="product description" ,discount=10, cat=Cat.SHIRT, thumbnail='product_thumbnail.jpg', amt_left=5, gallery=['second_img.jpg', 'first_img.jpg'], created_at=datetime.now() )), session: AsyncSession = Depends(get_async_session)): 
    fetched_cat = await get_category_by_name(new_product.cat) 
    product = Product(**new_product.model_dump(exclude_unset=True), cat=fetched_cat)
    session.add(product) 
    await session.commit()   
    return product


@router.get('/', response_model=list[ProductRead])
async def get_all_products(): 
    products = await get_products()
    return products

@router.get('/{id}', response_model=ProductRead)
async def get_product_by_id(product: Product = Depends(get_product_or_404)): 
    return product

@router.get('/{cat}')
async def get_products_by_category(cat: Cat = Query(example=Cat.SHIRT), session: AsyncSession = Depends(get_async_session)): 
    category = await get_category_by_name(cat)
    q = select(Product).where(Product.cat_id == category.id)
    return (await session.scalars(q)).all()      

@router.get('/group_by_cat')
async def get_products_group_by_cat(session: AsyncSession = Depends(get_async_session)): 
    q = select(Product, Category.name.label('category'), func.count(Product.id).label('num_products')).join(Category.products).group_by(Category.name).order_by(Category.name)
    return (await session.execute(q)).all()

#TODO: For admins and merchants only
@router.patch('/{id}' , dependencies=[ Depends(get_curr_user), Depends(Rbac(role=[Role.DEVELOPER, Role.MERCHANT]).accessible_to)], status_code=status.HTTP_200_OK)
async def update_product(id: int,  prod_updates: ProductUpdate = Body(...), session: AsyncSession = Depends(get_async_session)) -> bool:
    if not prod_updates: 
        raise HTTPException(status_code=400, detail="You must update at least a field")
    q =  update(Product).where(Product.id == id).values(**prod_updates.model_dump( exclude_unset=True ))
    res = await session.execute(q)
    await session.commit() 
    if res.rowcount == 0: 
        return False 
    return True 

# TODO: For admins and merchants only
@router.delete('/{id}',dependencies=[ Depends(get_curr_user), Depends(Rbac(role=[Role.DEVELOPER, Role.MERCHANT]).accessible_to)] ,status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(id: int, session: AsyncSession = Depends(get_async_session)) -> bool: 
    q =  delete(Product).where(Product.id == id) 
    res = await session.execute(q)
    await session.commit() 
    if res.rowcount == 0: 
        return False 
    return True 

