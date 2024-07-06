#!/usr/bin/env python3
"""order model"""
from models.base import Base, BaseModel
from sqlalchemy import (
    Column, String, Integer, ForeignKey
)


class Order(BaseModel, Base):
    """class Order"""
    __tablename__ = "orders"

    # data order
    status = Column(String(40), default="pending")
    quantity = Column(Integer, nullable=False, default=1)
    total_price = Column(Integer, nullable=True)
    orderValid = Column(Integer, default=0, nullable=False)

    # foreign key
    user_id = Column(
        Integer, ForeignKey('users.id'),
        nullable=False
    )
    product_id = Column(
        Integer, ForeignKey('products.id'),
        nullable=False
    )
