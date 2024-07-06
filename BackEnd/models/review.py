#!/usr/bin/env python3
"""review model"""
from models.base import Base, BaseModel
from sqlalchemy import (
    Column, String, Integer, ForeignKey, TEXT
)


class Review(BaseModel, Base):
    """class review"""
    __tablename__ = "reviews"

    rating = Column(Integer, nullable=False)
    comment = Column(String(255), nullable=True)
    images = Column(TEXT, nullable=True)

    # foreignkey
    product_id = Column(
        Integer, ForeignKey('products.id'), nullable=False
    )
    user_id = Column(
        Integer, ForeignKey('users.id'), nullable=False
    )
