from fastapi import APIRouter, Depends, status, Body 
from ..db.schema import ReviewCreate, ReviewRead, ReviewUpdate
from ..db.db_conn import AsyncSession, get_async_session
from sqlalchemy import select, update, delete 
from .product import get_product_or_404, Product

router = APIRouter(prefix='/review', tags=['reviews'])

@router.get('/product/{id}', response_model=list[ReviewRead] | None)
async def get_reviews_by_prod(product: Product = Depends(get_product_or_404), session: AsyncSession = Depends(get_async_session)): 
    return product.reviews

