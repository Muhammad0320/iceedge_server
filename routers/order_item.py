from fastapi import APIRouter, Depends, status, HTTPException
from ..db.schema import ReviewCreate, ReviewRead, ReviewUpdate
from ..db.db_conn import AsyncSession, get_async_session
from ..db.model import  Product, OrderItem, User, Order
from sqlalchemy import select, update, delete 
# from .product import get_product_or_404

router = APIRouter(prefix='/order_item', tags=['order', 'item'])

async def get_item_or_404(id: int, session: AsyncSession = Depends(get_async_session)) -> OrderItem: 
    result = (await  session.scalars(select(OrderItem).where(OrderItem.id == id))).one_or_none()
    if not result: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Order item not found')
    return result

async def get_order_or_404(id: int, session: AsyncSession = Depends(get_async_session)) -> Order: 
    result = (await session.scalars(select(Order, OrderItem ).where(Order.id == id))).one_or_none() 
    if not result: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Order not found')
    return result
    
@router.get('/{id}', response_model=OrderItem) 
async def get_item_by_id(item: OrderItem = Depends(get_item_or_404), session: AsyncSession = Depends(get_async_session)):
    return item

# TODO: Only Admins and Developer
@router.get('/', response_model=list[OrderItem])
async def get_all_items(session: AsyncSession = Depends(get_async_session)): 
    result = (await session.scalars(select(OrderItem))).all() 
    return result
    
@router.get('/order/{id}', response_model=list[OrderItem])
async def get_items_by_order( order: Order = Depends(get_order_or_404), session: AsyncSession = Depends(get_async_session)): 
    return order 

