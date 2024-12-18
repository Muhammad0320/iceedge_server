from fastapi import APIRouter, Depends, status, Body, HTTPException, Path
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

@router.get('/{id}', response_model=ReviewRead)
async def get_review(review: Review = Depends(get_review_or_404)): 
    return review

@router.patch('/{id}')
async def update_review(id: int = Path(...), updates: ReviewUpdate = Body(example=ReviewUpdate(rating=5.0, content='new rating')), session: AsyncSession = Depends(get_async_session)): 
    if not updates: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='You must at least update a field!')
    q = update(Review).where(Review.id == id).values(**updates.model_dump(exclude_unset=True))
    result = await session.execute(q) 
    await session.commit() 
    if result.rowcount == 0: 
        return False 
    return True 

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT) 
async def delete_review(id: int = Path(...), session: AsyncSession = Depends(get_async_session)): 
    q = delete(Review).where(Review.id == id) 
    result = await session.execute(q) 
    if result.rowcount == 0: 
        return False 
    return True