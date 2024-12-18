from fastapi import APIRouter, Depends, status, HTTPException
from ..db.db_conn import AsyncSession, get_async_session
from ..db.model import  Product, CartItem, User, Cart 
from sqlalchemy import select, update, delete 
from sqlalchemy.orm import joinedload


router = APIRouter(prefix='/cart', tags=['cart', 'item'])

async def get_cart_by_user(id: int, session: AsyncSession = Depends(get_async_session)): 
    q = select(Cart).where(Cart.user_id == id)
    result = (await session.execute(q)).one_or_none()
    if not result: 
        return None 
    return result


    