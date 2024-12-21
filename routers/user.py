from fastapi import APIRouter, Form, Depends, status, HTTPException, Body, Query, Path, Response
from sqlalchemy import select, and_
from sqlalchemy.orm import joinedload
from ..db.model import User, AccessToken
from sqlalchemy.exc import IntegrityError
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer, APIKeyCookie
from ..security.password import hash_password
from ..db.schema import UserCreate, Message, UserRead, Credential
from datetime import datetime, timezone
from ..db.db_conn import AsyncSession, get_async_session
from ..security.authenticate import authenticate, create_access_token
from ..main import TOKEN_COOKIE_NAME


router = APIRouter(prefix='/user', tags=['users']) 

async def get_current_user_by_token(token_str: str = Depends(OAuth2PasswordBearer(tokenUrl='/token')), session: AsyncSession = Depends(get_async_session)):
    q = select(AccessToken).where(and_(AccessToken.token == token_str, AccessToken.expiration_date == datetime.now(tz=timezone.utc)))
    token = (await session.scalars(q)).one_or_none() 
    if not token: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED) 
    return token.user 

@router.post('/register', response_model=UserRead)
async def register_user(user: UserCreate, session: AsyncSession = Depends(get_async_session)): 
    hashed_password = hash_password(user.password)
    updated_object = User(**user.model_dump(exclude={'password'}), password=hashed_password) 
    try: 
        session.add(updated_object)
        await session.commit()
    except IntegrityError: 
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)  
    return updated_object

@router.post('/token', response_model=UserRead)
async def signin(credential: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm), session: AsyncSession = Depends(get_async_session)): 
    email = credential.username; password = credential.password
    user = await authenticate(Credential(email=email, password=password), session) 
    if not user: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid signin credentials")
    token = await create_access_token(user, session) 
    return {"access_token": token.token, "token_type": "bearer"}

@router.post('/login')
async def login(response: Response, email: str = Form(...), password: str = Form(...), session: AsyncSession = Depends(get_async_session)): 
    user = await authenticate(Credential(email=email, password=password), session=session) 
    if not user: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    token = await create_access_token(user=user, session=session)
    response.set_cookie(
        TOKEN_COOKIE_NAME,
        token.token, 
        max_age=token.max_age(),
        samesite='lax',
        secure=True, 
        httponly=True
    )    

@router.get('/me', response_model=User)
async def get_current_user(token: str = Depends(APIKeyCookie(name=TOKEN_COOKIE_NAME)), session: AsyncSession = Depends(get_async_session)): 
    user = await get_current_user_by_token(token_str=token) 
    return user     
