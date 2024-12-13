from fastapi import FastAPI
from contextlib import asynccontextmanager
from .db.db_conn import create_all_tables
from .routers import product

@asynccontextmanager
async def lifespan(app: FastAPI): 
    await create_all_tables() 
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(router=product.router)