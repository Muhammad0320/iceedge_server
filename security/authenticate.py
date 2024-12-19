from fastapi import Depends, HTTPException, status
from .password import verify_password, hash_password 
from ..db.db_conn import get_async_session, AsyncSession
from ..db.schema import Authenticate
from ..db.model import User
from sqlalchemy import select



async def authenticate(user: Authenticate, session: AsyncSession = Depends(get_async_session)): 
    q = select(User).where(User.email == user.email)
    db_user = (await session.execute(q)).one_or_none() 
    
    if not db_user: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Password or username is invalid')

    is_valid_passsword = verify_password(user.password, db_user.password) 
    
    if not is_valid_passsword: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Password or username is invalid')    
    return db_user 

