from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import DateTime, String, Text, Integer, Float, JSON, Enum 

class Base(DeclarativeBase):
    pass 

class Role(Enum): 
    ADMIN = 'admin'
    CUSTOMER = 'customer' 
    DEVELOPER = 'developer'

class Product(Base): 
    __tablename__='product'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    price: Mapped[float] = mapped_column(Float, nullable=False) 
    discount: Mapped[float] = mapped_column(Float, default=0) 
    name: Mapped[str] = mapped_column(String(255), nullable=False) 
    description: Mapped[str] = mapped_column(Text, nullable=False) 
    thumbnail: Mapped[str] = mapped_column(String(255), nullable=False)
    gallery: Mapped[list[str]] = mapped_column(JSON, nullable=False) 
    amt_left: Mapped[int] = mapped_column(Integer, nullable=False)  
    avg_rating: Mapped[float] = mapped_column(Float, default=0) 
    ratings_count: Mapped[int] = mapped_column(Float, default=0) 
    
    
class Customer(Base): 
    __tablename__='customer'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True) 
    firstname: Mapped[str] = mapped_column(String(255), nullable=False) 
    lastname: Mapped[str] = mapped_column(String(255), nullable=False)  
    email: Mapped[str] = mapped_column(String(255), nullable=False) 
    password: Mapped[str] = mapped_column(String(255), nullable=False) 
    role: Mapped[Role] = mapped_column(Enum(Role), default=Role.CUSTOMER) 
    shipping_address: Mapped[str] = mapped_column(Text, nullable=False) 

class Review(Base): 
    __tablename__ = 'review'
    
    