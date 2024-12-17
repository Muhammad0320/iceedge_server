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

class Message: 
    detail: str = "Something went wrong!"

class OrderStatus(str, Enum): 
    DELIVERED='delivered'
    CANCELLED='cancelled'
    PENDING='pending'

class ProductBase(BaseModel): 
    price: float = Field(..., ge=2999.99) 
    discount: int = Field(..., ge=0, le=99) 
    name: str 
    description: str 
    thumbnail: str 
    gallery: list[str] 
    amt_left: int = Field(..., ge=1) 
    created_at: datetime = Field(default_factory=datetime.now)
    cat: Cat 
    class Config:
        orm_mode=True 

class ProductCreate(ProductBase): 
    pass 

class ProductRead(ProductBase): 
    id: int  
    avg_rating: float = Field(0, ge=1.0, le=5.0)
    ratings_count: int = Field(0, ge=0)
    reviews: list["ReviewRead"] | None = Field(None) 

class ProductUpdate(BaseModel): 
    discount:  int | None = Field(None, ge=0, le=99) 
    name:  str | None = Field(None) 
    price:  float | None = Field(None) 
    description:  str | None = Field(None) 
    category:  Cat | None = Field(None) 
    thumbnail:  str | None = Field(None) 
    gallery: list[str | None] = Field(None) 
    amt_left:  int | None = Field(None, ge=1) 
    avg_rating:  float | None = Field(None, ge=1.0, le=5.0)
    ratings_count:  int | None = Field(None, ge=0)

class UserBase(BaseModel): 
    firstname: str 
    lastname: str 
    email: EmailStr 
    password: str = Field(..., min_length=8) 
    password_confirm: str 
    shipping_address: str 
    created_at: datetime = Field(default_factory=datetime.now) 
    class Config: 
        orm_mode=True 
    
class UserCreate(UserBase): 
    @model_validator(mode='after') 
    def validate_password(self) -> Self:
        if self.password != self.password_confirm: 
            raise ValueError("Passwords must match!") 
        return self

class UserRead(UserBase): 
    id: int 
    role: Role = Field(default=Role.CUSTOMER)  
    orders: list["OrderRead"] | None = Field(None) 
    
    
class UserUpdate(BaseModel): 
    firstname: str | None = Field(None)  
    lastname: str | None = Field(None)
    email: EmailStr | None = Field(None)
    password: str | None = Field(None, min_length=8) 
    password_confirm: str | None = Field(None)
    shipping_address: str | None = Field(None)

class ReviewBase(BaseModel): 
    content: str 
    rating: float = Field(0, ge=1.0, le=5.0)
    created_at: datetime = Field(default_factory=datetime.now) 
    product_id: int 
    class Config:
        orm_mode=True 

class ReviewCreate(ReviewBase): 
    pass 

class ReviewRead(ReviewBase): 
    id: int 
    num_marked_useful: int = Field(0)
    user: UserRead
    
    
class ReviewUpdate(BaseModel): 
    content: str | None = Field(None)
    rating: float | None = Field(None, ge=1.0, le=5.0)

class OrderBase(BaseModel): 
    total: float = Field(..., ge=4999.99) 
    quantity: int = Field(..., gt=1) 
    shipping_fee: float 
    shipping_address: str 
    created_at: datetime = Field(default_factory=datetime.now) 
    customer_id: int 
    order_status: OrderStatus = Field(OrderStatus.PENDING)  
    order_items: list["ItemRead"]
    class Config:
        orm_mode=True 

class OrderCreate(OrderBase): 
    pass 

class OrderRead(OrderBase): 
    id: int 

class OrderUpdate(BaseModel): 
    total: float | None = Field(None, ge=4999.99) 
    quantity: int | None = Field(None, gt=1) 
    shipping_fee: float | None = Field(None)
    shipping_address: str | None = Field(None)

class CategoryBase(BaseModel): 
    name: Cat 
    class Config:
        orm_mode=True 

class CategoryCreate(CategoryBase): 
    pass 

class CategoryRead(CategoryBase): 
    id: int 
    products: list['ProductRead']

class CategoryUpdate(BaseModel): 
    name: Cat | None = Field(None)


class ItemBase(BaseModel): 
    total: float = Field(..., ge=4999.99) 
    quantity: int = Field(..., gt=1) 
    product_id: int 
    order_id: int 
    class Config:
        orm_mode=True 

class ItemCreate(ItemBase): 
    pass

class ItemRead(ItemBase): 
    id: int 

class ItemUpdate(BaseModel): 
    total: float | None = Field( None, ge=4999.99) 
    quantity: int | None = Field (None,  gt=1) 
