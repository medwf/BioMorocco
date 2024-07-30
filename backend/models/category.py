#!/usr/bin/env python3
"""product model"""
from models.base import Base, BaseModel
from sqlalchemy import (
    Column, String, Integer, ForeignKey, TEXT
)
from sqlalchemy.orm import relationship


class Category(BaseModel, Base):
    """class product"""
    __tablename__ = "categories"

    # data
    name = Column(String(45), nullable=False, unique=True)
    desc = Column(TEXT, nullable=True)
    benefit = Column(TEXT, nullable=True)
    image = Column(String(255), nullable=True)

    # relationship
    products = relationship(
        "Product", backref="category",
        cascade="all, delete, save-update")
