#!/usr/bin/env python3
"""product model"""
from models.base import Base, BaseModel
from sqlalchemy import (
    Column, String, Integer, ForeignKey, TEXT
)
from sqlalchemy.orm import relationship


class Product(Base, BaseModel):
    """class product"""
    __tablename__ = "products"

    name = Column(String(45), nullable=False, unique=True)
    desc = Column(TEXT, nullable=True)
    price = Column(Integer, nullable=False)
    stock = Column(Integer, nullable=False)
    reminder_stock = Column(Integer, nullable=False, default=10)
    images = Column(TEXT, nullable=False)

    # should add sum of rating in review / num of review
    total_rating = Column(Integer, nullable=True)
    location = Column(String(255), nullable=False)

    # make table for category
    category_id = Column(Integer, ForeignKey(
        'categories.id'), nullable=False
    )

    store_id = Column(Integer, ForeignKey(
        'stores.id'), nullable=False
    )

    # relationship
    cartItems = relationship(
        'CartItem', backref='product',
        cascade='all, delete, save-update'
    )

    orderItems = relationship(
        'OrderItem', backref='product',
        cascade='save-update, merge, refresh-expire, expunge'
    )

    reviews = relationship(
        'Review', backref='product',
        cascade='save-update, merge, refresh-expire, expunge'
    )
