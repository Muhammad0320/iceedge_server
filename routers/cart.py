from fastapi import APIRouter, Depends, status, HTTPException
from ..db.db_conn import AsyncSession, get_async_session
from ..db.model import  Product, CartItem, User, Cart 
from sqlalchemy import select, update, delete 
from sqlalchemy.orm import joinedload


router = APIRouter(prefix='/cart', tags=['cart', 'item'])

async def get_cart_by_user(id: int, session: AsyncSession = Depends(get_async_session)): 
    q = select(Cart).where(Cart.user_id == id).order_by(Cart.created_at)
    result = (await session.execute(q)).one_or_none()
    if not result: 
        return None 
    return result

async def get_cart_or_none(id: int, session: AsyncSession = Depends(get_async_session)): 
    q = select(Cart).where(Cart.id == id).order_by(Cart.created_at)
    result = (await session.execute(q)).one_or_none() 
    if not result: 
        return None 
    return result

@router.get('/user/{id}', response_model=Cart) 
async def get_cart_by_user_id(cart: Cart = Depends(get_cart_by_user)): 
    return cart 

# TODO: For developer only
@router.get('/')
async def get_all_carts(session: AsyncSession = Depends(get_async_session)): 
    q = select(Cart).order_by(Cart.created_at)
    return (await session.execute(q) ).all() 

