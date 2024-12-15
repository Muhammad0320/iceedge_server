from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy import DateTime, String, Text, Integer, Float, JSON, Enum, ForeignKey
from datetime import datetime
from typing import List, Optional

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

class OrderStatus(Enum): 
    DELIVERED='delivered'
    CANCELLED='cancelled'
    PENDING='pending'

class Product(Base): 
    __tablename__='products'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    price: Mapped[float] = mapped_column(Float) 
    discount: Mapped[float] = mapped_column(Floatdefault=0) 
    name: Mapped[str] = mapped_column(String(255), unique=True)  
    description: Mapped[str] = mapped_column(Text) 
    cat_id: Mapped[int] = mapped_column(ForeignKey('category.id'), index=True) 
    thumbnail: Mapped[str] = mapped_column(String(255))
    gallery: Mapped[list[str]] = mapped_column(JSON) 
    amt_left: Mapped[int] = mapped_column(Integer)  
    avg_rating: Mapped[float] = mapped_column(Float, default=0) 
    ratings_count: Mapped[int] = mapped_column(Float, default=0) 
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now) 
    reviews: Mapped[Optional[List["Review"]]] = relationship("Review", cascade='all, delete') 
    cat: Mapped['Category'] = relationship(back_populates='products')

class User(Base): 
    __tablename__='users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True) 
    firstname: Mapped[str] = mapped_column(String(32)) 
    lastname: Mapped[str] = mapped_column(String(32))  
    role: Mapped[Role] = mapped_column(Enum(Role), default=Role.CUSTOMER) 
    email: Mapped[str] = mapped_column(String(64), unique=True)  
    password: Mapped[str] = mapped_column(String(255)) 
    shipping_address: Mapped[ Optional[str]] = mapped_column(Text) 
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now) 
    orders: Mapped[Optional[List["Order"]]] = relationship("Order", cascade='all, delete')
    

class Review(Base): 
    __tablename__ = 'reviews'
    id: Mapped[int] = mapped_column(Integer, primary_key=True) 
    content: Mapped[str] = mapped_column(Text)     
    rating: Mapped[float] = mapped_column(Float, max=5.0, min=1.0) 
    num_marked_useful: Mapped[int] = mapped_column(Integer, default=0) 
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now) 
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'), index=True)  
    product: Mapped["Product"] = relationship("Product", back_populates='reviews') 
    

class Order(Base): 
    __tablename__= "orders"
    id: Mapped[int] = mapped_column(Integer, primary_key=True) 
    total: Mapped[float] = mapped_column(Integer) 
    quantity: Mapped[int] = mapped_column(Integer, default=1) 
    shipping_fee: Mapped[float] = mapped_column(Float) 
    status: Mapped[OrderStatus] = mapped_column(OrderStatus) 
    shipping_address: Mapped[Optional[str]] = mapped_column(String(255)) 
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now) 
    customer_id: Mapped[int] = mapped_column(ForeignKey('user.id')) 
    customer: Mapped["User"] = relationship("User", back_populates="orders") 
    order_items: Mapped[List['Item']] = relationship("Item") 


# class Cart(Base): 
#     __tablename__= "carts"
#     id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True) 
#     total: Mapped[float] = mapped_column(Float, nullable=False) 
    
#     created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now) 

class Category(Base): 
    __tablename__= "categories"
    id: Mapped[int] = mapped_column(Integer, primary_key=True) 
    name: Mapped[Cat] = mapped_column(Enum(Cat), unique=True, index=True) 
    products: Mapped[List["Product"]] = relationship(back_populates='cat')

class Item(Base): 
    __tablename__= "items"
    id: Mapped[int] = mapped_column(Integer, primary_key=True) 
    total: Mapped[float] = mapped_column(Float) 
    quantity: Mapped[int] = mapped_column(Integer, default=1) 
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id')) 
    product: Mapped['Product'] = relationship("Product") 
    order_id: Mapped[int] = mapped_column(ForeignKey('order.id'), index=True)