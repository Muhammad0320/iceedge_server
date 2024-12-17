from fastapi import APIRouter, Depends, status, HTTPException
from ..db.schema import ReviewCreate, ReviewRead, ReviewUpdate
from ..db.db_conn import AsyncSession, get_async_session
from ..db.model import  Product, Item
from sqlalchemy import select, update, delete 
from .product import get_product_or_404

router = APIRouter(prefix='/item', tags=['order', 'item'])

