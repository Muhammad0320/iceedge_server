from fastapi import APIRouter, Depends, status, HTTPException
from ..db.db_conn import AsyncSession, get_async_session
from ..db.model import  Product, OrderItem, User, Order
from sqlalchemy import select, update, delete 
from sqlalchemy.orm import joinedload


router = APIRouter(prefix='/cart', tags=['cart', 'item'])
