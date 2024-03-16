import uuid
from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON, Float
from sqlalchemy.ext.declarative import DeferredReflection
from sqlalchemy.orm import declarative_base

from .db_engine import DBEngine

Base = declarative_base(cls=DeferredReflection)


def generate_uuid():
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = 'user'
    user_id = Column(String(50), default=generate_uuid(), primary_key=True)
    username = Column(String(50), unique=True)
    email = Column(String(50))
    password = Column(String(50))
    first_name = Column(String(50))
    last_name = Column(String(50))
    role = Column(String(50))
    user_metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, onupdate=datetime.now())
    status = Column(String)


class Category(Base):
    __tablename__ = 'category'
    category_id = Column(String(50), default=generate_uuid(), primary_key=True)
    name = Column(String(50))
    description = Column(String(50))
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, onupdate=datetime.now())
    status = Column(String)
    # metadata = Column(JSON)
    image_path = Column(String(255))


class Product(Base):
    __tablename__ = 'product'
    product_id = Column(String(50), default=generate_uuid(), primary_key=True)
    category_id = Column(String(50), ForeignKey('category.category_id'))
    name = Column(String(50))
    description = Column(String(50))
    status = Column(String)
    stock = Column(Integer)
    price = Column(Integer)
    weight = Column(Float)
    image_path = Column(String(50))
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, onupdate=datetime.now())


class Address(Base):
    __tablename__ = 'address'
    address_id = Column(String(50), default=generate_uuid(), primary_key=True)
    user_id = Column(String(50), ForeignKey('user.user_id'))
    address = Column(String(50))
    city = Column(String(50))
    state = Column(String(50))
    pincode = Column(String(50))
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, onupdate=datetime.now())


class Order(Base):
    __tablename__ = 'order'
    order_id = Column(String(50), default=generate_uuid(), primary_key=True)
    user_id = Column(String(50), ForeignKey('user.user_id'))
    order_info = Column(JSON)
    status = Column(String(50))
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, onupdate=datetime.now())


def create_db_models():
    engine = DBEngine.get_db_engine()
    Base.metadata.create_all(engine, Base.metadata.tables.values(), checkfirst=True)
    Base.prepare(engine)
