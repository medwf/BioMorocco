#!/usr/bin/env python3
"""Store model"""
from models.base import Base, BaseModel
from sqlalchemy import (
    Column, String, Integer, ForeignKey, TEXT
)
from sqlalchemy.orm import relationship


class Store(BaseModel, Base):
    """class product"""
    __tablename__ = "stores"

    # data
    name = Column(String(50), nullable=False, unique=False)
    description = Column(TEXT, nullable=False)
    image = Column(String(255), nullable=True)

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    # relationship
    categories = relationship(
        "Category", backref="store",
        cascade="all, delete, save-update")
