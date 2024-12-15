from fastapi import APIRouter, Depends, status, Body, HTTPException
from ..db.schema import ReviewCreate, ReviewRead, ReviewUpdate
from ..db.db_conn import AsyncSession, get_async_session
from ..db.model import Review, Product
from sqlalchemy import select, update, delete 
from .product import get_product_or_404

router = APIRouter(prefix='/review', tags=['reviews'])

async def get_review_or_404(id: int, session: AsyncSession = Depends(get_async_session)): 
    result = (await session.scalars(select(Review).where(Review.id == id))).one_or_none() 
    if not result: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Review you requested is not found!')
    return result
@router.get('/product/{id}', response_model=list[ReviewRead] | None)
async def get_reviews_by_prod(product: Product = Depends(get_product_or_404)): 
    return product.reviews

@router.post('/', response_model=ReviewRead, status_code=status.HTTP_201_CREATED)
async def create_post(new_review: ReviewCreate = Body(example=ReviewCreate(content="The best", rating=5.0, product_id=999)), session: AsyncSession = Depends(get_async_session)): 
    review = Review(**new_review.model_dump(exclude_unset=True))
    session.add(review)
    await session.commit() 
    return review
