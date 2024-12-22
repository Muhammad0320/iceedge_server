from .db.model import AccessToken
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select, and_ 
from .db.schema import Role
from .db.model import User 
from fastapi.security import APIKeyCookie
from fastapi import Depends, status, HTTPException
from .db.db_conn import AsyncSession, get_async_session
from datetime import timezone, datetime
from .main import TOKEN_COOKIE_NAME

async def get_current_user_by_token(token_str: str = Depends(OAuth2PasswordBearer(tokenUrl='/token')), session: AsyncSession = Depends(get_async_session)):
    q = select(AccessToken).where(and_(AccessToken.token == token_str, AccessToken.expiration_date == datetime.now(tz=timezone.utc)))
    token = (await session.scalars(q)).one_or_none() 
    if not token: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED) 
    return token.user 

async def get_curr_user(token: str = Depends(APIKeyCookie(name=TOKEN_COOKIE_NAME))): 
    user = await get_current_user_by_token(token_str=token) 
    return user

async def role_is_in(role: list[Role], user: User): 
    if not user.role in role: 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return True  
    

async def accessible_to(role: list[Role], user: User = Depends(get_curr_user)):
     return ( await role_is_in(role=role, user=user) )
