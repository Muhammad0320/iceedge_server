from fastapi import FastAPI
from contextlib import asynccontextmanager
from .db.db_conn import create_all_tables
from .routers import product
from .routers import review

@asynccontextmanager
async def lifespan(app: FastAPI): 
    await create_all_tables() 
    yield

app = FastAPI(lifespan=lifespan)

@app.get('/hello')
async def welcome(): 
    return "Welcome to Iceedge, what do you need?"

app.include_router(router=product.router)
app.include_router(router=review.router)