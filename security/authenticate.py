from fastapi import  HTTPException, status
from .password import verify_password
from ..db.db_conn import AsyncSession
from ..db.schema import Credential
from ..db.model import User, AccessToken
from sqlalchemy import select


async def authenticate(user: Credential, session: AsyncSession ) -> User | None : 
    q = select(User).where(User.email == user.email)
    db_user = (await session.scalars(q)).one_or_none() 
    
    if not db_user: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Password or username is invalid')

    is_valid_passsword = verify_password(user.password, db_user.password) 
    
    if not is_valid_passsword: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Password or username is invalid')    

    return db_user 

async def create_access_token(user: User, session: AsyncSession): 
    token = AccessToken(user=user)
    session.add(token) 
    await session.commit() 
    return token 
