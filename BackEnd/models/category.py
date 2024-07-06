#!/usr/bin/env python3
"""product model"""
from models.base import Base, BaseModel
from sqlalchemy import (
    Column, String, Integer, ForeignKey
)
from sqlalchemy.orm import relationship


class Category(BaseModel, Base):
    """class product"""
    __tablename__ = "categories"

    # data
    name = Column(String(45), nullable=False, unique=True)
    description = Column(String(255), nullable=True)
    image = Column(String(255), nullable=True)
    store_id = Column(Integer, ForeignKey('stores.id'), nullable=False)

    # relationship
    products = relationship(
        "Product", backref="category",
        cascade="all, delete, save-update")
