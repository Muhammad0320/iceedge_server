from fastapi import APIRouter, Depends, status, HTTPException
from ..db.db_conn import AsyncSession, get_async_session
from ..db.model import  Product, OrderItem, User, Order
from sqlalchemy import select, update, delete 
from sqlalchemy.orm import joinedload
# from .product import get_product_or_404

router = APIRouter(prefix='/order', tags=['order', 'item'])

async def get_item_or_404(id: int, session: AsyncSession = Depends(get_async_session)) -> OrderItem: 
    result = (await  session.scalars(select(OrderItem).where(OrderItem.id == id))).one_or_none()
    if not result: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Order item not found')
    return result

async def get_order_or_404(id: int, session: AsyncSession = Depends(get_async_session)) -> Order: 
    result = (await session.scalars(select(Order, OrderItem ).where(Order.id == id).options(joinedload(Order.order_items)))).one_or_none() 
    if not result: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Order not found')
    return result

async def get_user_orders_or_404(id: int, session: AsyncSession = Depends(get_async_session)): 
    result = (await session.scalars(select(Order).where(Order.customer == id).options(joinedload(Order.order_items)))).all() 
    if not result: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Order not found')
    return result
    
@router.get('/items/{id}', response_model=OrderItem) 
async def get_item_by_id(item: OrderItem = Depends(get_item_or_404), session: AsyncSession = Depends(get_async_session)):
    return item


# TODO: Only Admins and Developer
@router.get('/items', response_model=list[OrderItem])
async def get_all_items(session: AsyncSession = Depends(get_async_session)): 
    result = (await session.scalars(select(OrderItem))).all() 
    return result

    
@router.get('/{id}', response_model=list[OrderItem])
async def get_items_by_order( order: Order = Depends(get_order_or_404), session: AsyncSession = Depends(get_async_session)): 
    return order 

# TODO: Only admin and developer
@router.get('/', response_model=list[OrderItem])
async def get_all_order(session: AsyncSession = Depends(get_async_session)): 
    result = (await session.scalars(select(Order))).all()
    return result

@router.get('/user/{id}')
async def get_order_by_user(order = Depends(get_user_orders_or_404)): 
    return order
