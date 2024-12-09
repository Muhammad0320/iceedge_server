from pydantic import BaseModel, EmailStr, model_validator, Field
from datetime import datetime
from enum import Enum 
from typing_extensions import Self

class Role(str, Enum): 
    ADMIN = 'admin'
    CUSTOMER = 'customer' 
    DEVELOPER = 'developer'

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
    created_at: datetime = Field(default_factory=datetime.now)


class ProductCreate(ProductBase): 
    pass 

class ProductRead(ProductBase): 
    id: int 

class ProductUpdate(BaseModel): 
    discount: int = Field(None, ge=0, le=99) 
    name: str = Field(None) 
    description: str = Field(None) 
    category: Cat = Field(None) 
    thumbnail: str = Field(None) 
    gallery: list[str] = Field(None) 
    amt_left: int = Field(None, ge=1) 
    avg_rating: float = Field(None, ge=1.0, le=5.0)
    ratings_count: int = Field(None, ge=0)

class UserBase(BaseModel): 
    firstname: str 
    lastname: str 
    email: EmailStr 
    password: str = Field(..., min_length=8) 
    password_confirm: str 
    shipping_address: str 
    role: Role = Field(default=Role.CUSTOMER)  
    created_at: datetime = Field(default_factory=datetime.now) 

class UserCreate(UserBase): 
    @model_validator(mode='after') 
    def validate_password(self) -> Self:
        if self.password != self.password_confirm: 
            raise ValueError("Passwords must match!") 
        return self

class UserRead(UserBase): 
    id: int 

class UserUpdate(BaseModel): 
    firstname: str = Field(None)  
    lastname: str = Field(None)
    email: EmailStr = Field(None)
    password: str = Field(None, min_length=8) 
    password_confirm: str = Field(None)
    shipping_address: str = Field(None)
