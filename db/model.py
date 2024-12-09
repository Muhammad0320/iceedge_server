from pydantic import BaseModel, EmailStr, model_validator, Field
from datetime import datetime
from enum import Enum 

class Cat(str, Enum): 
    SHIIRT = "shirt"
    PANT = 'pant'
    CAP = 'cap'
    SHOE = 'shoe'
    SOCK = 'sock'
    MASK = "mask"


class ProductBase(BaseModel): 
    price: float = Field(..., ge=2999.99) 
    discount: int = Field(..., ge=0, le=99) 
    name: str 
    description: str 
    category: Cat 
    thumbnail: str 
    gallery: list[str] 
    amt_left: int = Field(..., ge=1) 
    avg_rating: float = Field(0, ge=1.0, le=5.0)
    ratings_count: int = Field(0, ge=0)
    created_at: datetime


class ProductCreate(ProductBase): 
    pass 

class ProductRead(ProductBase): 
    id: int 