#!/usr/bin/python3
""" class User"""

from models.base import BaseModel, Base
from sqlalchemy import (
    Column, String, TEXT, Integer,
    ForeignKey
)
from sqlalchemy.orm import relationship
from bcrypt import hashpw, gensalt


class User(BaseModel, Base):
    """Representation of a user """
    __tablename__ = 'users'

    # data
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(64), nullable=False)

    first_name = Column(String(20), nullable=True)
    last_name = Column(String(20), nullable=True)
    image = Column(String(255), nullable=True)

    # relationship
    addresses = relationship(
        "Address",
        backref="user",
        cascade="all, delete, save-update")

    wishlists = relationship(
        "WishList", backref="user",
        cascade="all, delete, save-update")

    searches = relationship(
        "Search", backref="user",
        cascade="all, delete, save-update")

    store = relationship(
        "Store", backref="user", uselist=False,
        cascade="all, delete, save-update"
    )

    cartItems = relationship(
        "CartItem", backref="user",
        cascade="all, delete, save-update"
    )

    orders = relationship(
        "Order", backref="user",
        cascade="save-update, merge, refresh-expire, expunge"
    )
    reviews = relationship(
        "Review", backref="user",
        cascade="save-update, merge, refresh-expire, expunge"
    )

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        """sets a password with hashpw encryption"""
        if name == "password":
            value = hashpw(value.encode(), gensalt())
        super().__setattr__(name, value)


class Address(Base, BaseModel):
    """address for user"""
    __tablename__ = "addresses"

    country = Column(String(30), nullable=True)
    state = Column(String(30), nullable=True)
    city = Column(String(30), nullable=True)
    address = Column(TEXT, nullable=True)
    phone = Column(String(16), nullable=True)
    valid = Column(Integer, nullable=False, default=0)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)


class WishList(Base, BaseModel):
    """address for user"""
    __tablename__ = "wishlists"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)


class Search(Base, BaseModel):
    """address for user"""
    __tablename__ = "searches"

    name = Column(String(100), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
