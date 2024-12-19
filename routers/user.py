from fastapi import APIRouter, Depends, status, HTTPException, Body, Query, Path
from sqlalchemy import select, update, delete, func
from sqlalchemy.orm import joinedload
from ..db.model import Category, Product
from ..db.schema import ProductCreate, ProductRead, ProductUpdate, Message, Cat
from datetime import datetime
from ..db.db_conn import AsyncSession, get_async_session

router = APIRouter(prefix='/user', tags=['users']) 

