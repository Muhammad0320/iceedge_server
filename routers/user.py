from fastapi import APIRouter, Depends, status, HTTPException, Body, Query, Path
from sqlalchemy import select, update, delete, func
from sqlalchemy.orm import joinedload
from ..db.model import User
from ..security.password import hash_password
from ..db.schema import UserCreate, Message, UserRead
from datetime import datetime
from ..db.db_conn import AsyncSession, get_async_session

router = APIRouter(prefix='/user', tags=['users', 'all']) 

@router.post('/register', response_model=UserRead)
async def register_user(user: UserCreate, session: AsyncSession = Depends(get_async_session)): 
    hashed_password = hash_password(user.password)
    updated_object = User(**user.model_dump(exclude={'password'}), password=hashed_password) 
    session.add(updated_object)
    await session.commit() 
    return updated_object