#!/usr/bin/env python3
"""Cart nd cart item  model"""
from models.base import Base, BaseModel
from sqlalchemy import (
    Column, Integer, ForeignKey
)


class CartItem(Base, BaseModel):
    """class cart items"""
    __tablename__ = "cartItems"

    quantity = Column(Integer, nullable=False, default=1)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
