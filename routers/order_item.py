from fastapi import APIRouter, Depends, status, HTTPException
from ..db.schema import ReviewCreate, ReviewRead, ReviewUpdate
from ..db.db_conn import AsyncSession, get_async_session
from ..db.model import  Product, Item, User 
from sqlalchemy import select, update, delete 
# from .product import get_product_or_404

router = APIRouter(prefix='/items', tags=['order', 'item'])

async def get_item_or_404(id: int, session: AsyncSession = Depends(get_async_session)) -> Item: 
    result = (await  session.scalars(select(Item, Product.name, Product.thumbnail, Product.price).where(Item.id == id).join(Item.product, onclause=Item.product_id == Product.id))).one_or_none() 
    if not result: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found')
    return result

@router.get('/{id}', response_model=Item) 
async def get_item_by_id(item: Item = Depends(get_item_or_404), session: AsyncSession = Depends(get_async_session)):
    return item

# TODO: Only Admins and Developer
@router.get('/', response_model=list[Item])
async def get_all_items(session: AsyncSession = Depends(get_async_session)): 
    return (await session.scalars(select(Item))).all() 

