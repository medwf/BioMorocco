#!/usr/bin/python3
""" class User"""

from models.base import BaseModel, Base
from sqlalchemy import (
    Column, String, Integer, ForeignKey, Boolean
)
from sqlalchemy.orm import relationship
from bcrypt import hashpw, gensalt, checkpw


class User(BaseModel, Base):
    """Representation of a user """
    __tablename__ = 'users'

    # data
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(64), nullable=False)
    first_name = Column(String(20), nullable=True)
    last_name = Column(String(20), nullable=True)
    image = Column(String(255), nullable=True)
    phone = Column(String(16), nullable=True)
    country = Column(String(30), nullable=True)
    state = Column(String(30), nullable=True)
    city = Column(String(30), nullable=True)
    address = Column(String(255), nullable=True)

    # relationship
    reviews = relationship(
        "Review", backref="user",
        cascade="all, delete, save-update"
    )
    store = relationship(
        "Store", backref="user", uselist=False,
        cascade="all, delete, save-update"
    )
    orders = relationship(
        "Order", backref="user",
        cascade="all, delete, save-update"
    )
    cart = relationship(
        "Cart", backref="user", uselist=False,
        cascade="all, delete, save-update"
    )

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        """sets a password with hashpw encryption"""
        if name == "password":
            value = hashpw(value.encode(), gensalt())
        super().__setattr__(name, value)
