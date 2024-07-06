#!/usr/bin/env python3
"""Cart nd cart item  model"""
from models.base import Base, BaseModel
from sqlalchemy import (
    Column, String, Integer, ForeignKey, Boolean
)
from sqlalchemy.orm import relationship


class Cart(BaseModel, Base):
    """class cart"""
    __tablename__ = "carts"

    # data
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    # relationship
    cartItems = relationship(
        "CartItem", backref="cart",
        cascade="all, delete, save-update")


class CartItem(BaseModel, Base):
    """class cart items"""
    __tablename__ = "cartItems"

    quantity = Column(Integer, nullable=False)
    cart_id = Column(Integer, ForeignKey('carts.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
