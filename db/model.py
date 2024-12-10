from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy import DateTime, String, Text, Integer, Float, JSON, Enum, ForeignKey
from datetime import datetime
from typing import List
class Base(DeclarativeBase):
    pass 

class Role(Enum): 
    ADMIN = 'admin'
    CUSTOMER = 'customer' 
    DEVELOPER = 'developer'

class Cat(Enum): 
    SHIIRT = "shirt"
    PANT = 'pant'
    CAP = 'cap'
    SHOE = 'shoe'
    SOCK = 'sock'

class Product(Base): 
    __tablename__='products'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    price: Mapped[float] = mapped_column(Float, nullable=False) 
    discount: Mapped[float] = mapped_column(Float, default=0) 
    name: Mapped[str] = mapped_column(String(255), nullable=False) 
    description: Mapped[str] = mapped_column(Text, nullable=False) 
    cat_id: Mapped[int] = mapped_column(ForeignKey('category.id'), nullable=False)
    thumbnail: Mapped[str] = mapped_column(String(255), nullable=False)
    gallery: Mapped[list[str]] = mapped_column(JSON, nullable=False) 
    amt_left: Mapped[int] = mapped_column(Integer, nullable=False)  
    avg_rating: Mapped[float] = mapped_column(Float, default=0) 
    ratings_count: Mapped[int] = mapped_column(Float, default=0) 
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now) 
    reviews: Mapped[List["Review"]] = relationship("Review", cascade='all, delete') 
    

class User(Base): 
    __tablename__='users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True) 
    firstname: Mapped[str] = mapped_column(String(255), nullable=False) 
    lastname: Mapped[str] = mapped_column(String(255), nullable=False)  
    email: Mapped[str] = mapped_column(String(255), nullable=False) 
    password: Mapped[str] = mapped_column(String(255), nullable=False) 
    role: Mapped[Role] = mapped_column(Enum(Role), default=Role.CUSTOMER) 
    shipping_address: Mapped[str] = mapped_column(Text, nullable=False) 
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now) 
    orders: Mapped[List["Order"]] = relationship("Order", cascade='all, delete')
    

class Review(Base): 
    __tablename__ = 'reviews'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True) 
    content: Mapped[str] = mapped_column(Text, nullable=False)     
    rating: Mapped[float] = mapped_column(Float, nullable=False, max=5.0, min=1.0) 
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now) 
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'), nullable=False) 
    product: Mapped["Product"] = relationship("Product", back_populates='reviews' ) 
     

class Order(Base): 
    __tablename__= "orders"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True) 
    total: Mapped[float] = mapped_column(Integer, nullable=False) 
    quantity: Mapped[int] = mapped_column(Integer, default=1) 
    shipping_fee: Mapped[float] = mapped_column(Float, nullable=False) 
    shipping_address: Mapped[float] = mapped_column(Float, nullable=True) 
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now) 
    customer_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False) 
    customer: Mapped["User"] = relationship("User", back_populates="orders") 
    order_items: Mapped[List['Item']] = relationship("Item") 
    
# class Cart(Base): 
#     __tablename__= "carts"
#     id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True) 
#     total: Mapped[float] = mapped_column(Float, nullable=False) 
    
#     created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now) 

class Category(Base): 
    __tablename__= "categorys"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True) 
    name: Mapped[Cat] = mapped_column(Enum(Cat), nullable=False) 

class Item(Base): 
    __tablename__= "items"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True) 
    total: Mapped[float] = mapped_column(Float, nullable=False ) 
    quantity: Mapped[int] = mapped_column(Integer, default=1) 
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'), nullable=False) 
    product: Mapped[Product] = relationship("Product") 
    order_id: Mapped[int] = mapped_column(ForeignKey('order.id'), nullable=True)