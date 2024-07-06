#!/usr/bin/env python3
"""product model"""
from models.base import Base, BaseModel
from sqlalchemy import (
    Column, String, Integer, ForeignKey, TEXT
)
from sqlalchemy.orm import relationship


class Product(BaseModel, Base):
    """class product"""
    __tablename__ = "products"

    name = Column(String(45), nullable=False, unique=True)
    description = Column(String(255), nullable=True)
    price = Column(Integer, nullable=False)
    stock = Column(Integer, nullable=False)
    images = Column(TEXT, nullable=False)

    # should add sum of rating in review / num of review
    total_rating = Column(Integer, nullable=True)
    location = Column(String(255), nullable=False)

    # make table for category
    category_id = Column(Integer, ForeignKey(
        'categories.id'), nullable=False)

    # relationship
    cartItems = relationship(
        'CartItem', backref='product', cascade='all, delete, save-update')

    orders = relationship(
        'Order', backref='product', cascade='all, delete, save-update')

    reviews = relationship(
        'Review', backref='product', cascade='all, delete, save-update')
