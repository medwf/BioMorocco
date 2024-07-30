#!/usr/bin/env python3
"""order model"""
from models.base import Base, BaseModel
from sqlalchemy import (
    Column, String, Integer, ForeignKey
)
from sqlalchemy.orm import relationship


class Order(BaseModel, Base):
    """class Order"""
    __tablename__ = "orders"

    # data order
    total = Column(Integer, nullable=False)
    valid = Column(Integer, default=0, nullable=False)

    # foreign key
    user_id = Column(
        Integer, ForeignKey('users.id'),
        nullable=False
    )

    # Relationship
    orderItems = relationship(
        "OrderItem", backref="order",
        cascade="all, delete, save-update"
    )


class OrderItem(BaseModel, Base):
    """class Order"""
    __tablename__ = "orderItems"

    # data order
    quantity = Column(Integer, nullable=False, default=1)
    total_price = Column(Integer, nullable=True)
    # orderValid = Column(Integer, default=0, nullable=False)

    # foreign key
    # user_id = Column(
    #     Integer, ForeignKey('users.id'),
    #     nullable=False
    # )
    order_id = Column(
        Integer, ForeignKey('orders.id'),
        nullable=False
    )
    product_id = Column(
        Integer, ForeignKey('products.id'),
        nullable=False
    )
