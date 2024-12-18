from fastapi import FastAPI
from contextlib import asynccontextmanager
from .db.db_conn import create_all_tables
from .routers import order, product, review, cart, user

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
app.include_router(router=order.router)
app.include_router(router=cart.router)
app.include_router(router=user.router)