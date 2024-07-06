#!/usr/bin/env python3
"""database model"""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from models.base import Base
from models.user import User
from models.cart import Cart, CartItem
from models.order import Order
from models.review import Review
from models.product import Product
from models.category import Category
from models.store import Store
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {
    "Cart": Cart, "CartItem": CartItem,
    "Order": Order, "Review": Review,
    "Product": Product, "Category": Category,
    "User": User, "Store": Store
}


class DBStorage:
    """interact with the Mysql database"""

    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        BioMrc_USER = getenv('BioMrc_USER')
        BioMrc_PWD = getenv('BioMrc_PWD')
        BioMrc_HOST = getenv('BioMrc_HOST')
        BioMrc_DB = getenv('BioMrc_DB')
        BioMrc_ENV = getenv('BioMrc_ENV')
        self.__engine = create_engine(
            'mysql+pymysql://{}:{}@{}/{}?charset=utf8mb4'.format(
                BioMrc_USER, BioMrc_PWD,
                BioMrc_HOST, BioMrc_DB))
        if BioMrc_ENV == "test":
            Base.metadata.drop_all(self.___engine)

    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = f"{obj.__class__.__name__}.{obj.id}"
                    new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, id):
        """
        Returns the object based on the class name and its ID, or
        None if not found
        """
        import models
        if id is None or cls not in classes.values():
            return None

        return self.__session.query(User).filter_by(id=id).one()

    def count(self, cls=None):
        """
        count the number of objects in storage
        """
        all_class = classes.values()

        if not cls:
            count = 0
            for Class in all_class:
                count += len(self.all(Class).values())
        else:
            count = len(self.all(cls).values())
        return count

    def add_user(self, email: str, hashed_password: str) -> User:
        """add_user to add a new user in the db"""
        new_user = User(email=email, password=hashed_password)
        self.new(new_user)
        self.save()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """search for an user in database"""
        for key, value in kwargs.items():
            if hasattr(User, key):
                Filter = {key: value}
                return self.__session.query(User).filter_by(**Filter).one()
            else:
                raise InvalidRequestError()
        raise NoResultFound()

    def update_user(self, user_id: int, **kwargs) -> None:
        """update user in database based on id"""
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError
            setattr(user, key, value)
        self.save()
