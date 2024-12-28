from fastapi import APIRouter, Depends, status, Body, HTTPException, Path
from ..db.schema import ReviewCreate, ReviewRead, ReviewUpdate, Role
from ..db.db_conn import AsyncSession, get_async_session
from ..db.model import Review, Product, User
from sqlalchemy import select, update, delete, func 
from .product import get_product_or_404
from .order import check_if_user_purchase_prod
from .user import get_curr_user
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix='/review', tags=['reviews'])

async def check_if_mine(id: int, user: User, session: AsyncSession = Depends(get_async_session)): 
    review = await session.get(Review, id)
    if not review: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if (review.user_id != user.id) and user.role not in [Role.DEVELOPER, Role.ADMIN]: 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You can only modify your own review')
    return review


async def get_review_or_404(id: int, session: AsyncSession = Depends(get_async_session)): 
    result = (await session.scalars(select(Review).where(Review.id == id))).one_or_none() 
    if not result: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Review you requested is not found!')
    return result

@router.get('/product/{id}')
async def get_reviews_by_prod(id: int, session: AsyncSession = Depends(get_async_session)): 
    if not (await get_product_or_404(id, session)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    review_count = func.count(Review.id).label(None) 
    q = select(Product.name, Review, review_count).where(Product.id == id).join(Product.reviews).order_by(Review.created_at, Product.name) 
    res = (await session.scalars(q)).all()
    return res 

@router.post('/', dependencies=[Depends(get_curr_user)] ,response_model=ReviewRead, status_code=status.HTTP_201_CREATED)
async def create_post(user: User, new_review: ReviewCreate = Body(...,example=ReviewCreate(content="The best", rating=5.0, product_id=999)), session: AsyncSession = Depends(get_async_session)): 
    new_review.user_id = user.id 
    product_purchase = await check_if_user_purchase_prod(user.id, new_review.product_id, session) 
    if not product_purchase: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, status='You havr to purchase this product first')
    review = Review(**new_review.model_dump(exclude_unset=True))
    try: 
        session.add(review)
        await session.commit() 
        return review
    except IntegrityError: 
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Review already exist')

@router.get('/{id}', response_model=ReviewRead)
async def get_review(review: Review = Depends(get_review_or_404)): 
    return review
  
  
@router.patch('/{id}', dependencies=[Depends(get_curr_user), Depends(check_if_mine)])
async def update_review(id: int = Path(...), updates: ReviewUpdate = Body(example=ReviewUpdate(rating=5.0, content='new rating')), session: AsyncSession = Depends(get_async_session)): 
    if not updates: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='You must at least update a field!')
    q = update(Review).where(Review.id == id).values(**updates.model_dump(exclude_unset=True))
    result = (await session.execute(q) ).scalar_one() 
    await session.commit() 
    if result.rowcount == 0: 
        return False 
    return True 

@router.delete('/{id}',  dependencies=[Depends(get_curr_user), Depends(check_if_mine)] , status_code=status.HTTP_204_NO_CONTENT) 
async def delete_review(id: int = Path(...), session: AsyncSession = Depends(get_async_session)): 
    q = delete(Review).where(Review.id == id) 
    result = await session.execute(q) 
    await session.commit() 
    if result.rowcount == 0: 
        return False 
    return True 

