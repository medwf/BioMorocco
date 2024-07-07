#!/usr/bin/env python3
"""authentication module"""

# from models import storage
from models.engine.DBstorage import DBStorage
# from .auth import Auth
from bcrypt import checkpw
from models.user import User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from typing import List, Dict
from models import storage
from os import getenv

# def _hash_password(password: str) -> bytes:
#     """methods that hashed password"""
#     return hashpw(password.encode(), gensalt())


def _generate_uuid() -> str:
    """generate uuid based on uuid module"""
    from uuid import uuid4
    return str(uuid4())


class SessionDBAuth():
    """Auth class to interact with the authentication database.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require auth"""
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        # add allowing * of end of excluded path
        for exclude in excluded_paths:
            # print(f"\033[33m *1 {exclude} {path}\033[0m")
            if exclude[-1] != '*' or len(exclude[:-1]) > len(path):
                # print(f"\033[33m *2 {exclude} {path}\033[0m")
                continue
            exclude = exclude[:-1]
            # print(f"\033[33m *3 {exclude} {path}\033[0m")
            if exclude == path[:len(exclude)]:
                return False

        path = path if path[-1] == '/' else f'{path}/'
        if path in excluded_paths:
            return False
        return True

    def session_cookie(self, request=None):
        """Return a cookie value from a request"""
        if request is None:
            return None
        return request.cookies.get(getenv("SESSION_NAME", None), None)

    def current_user(self, request=None):
        """return an instance based on cookie value"""
        if request is None:
            return None
        session_id = self.session_cookie(request)
        if not session_id:
            return None
        user = self.get_user_from_session_id(session_id)
        return user if user else None

    def get_user_from_session_id(self, session_id: str) -> User:
        """get user based on session id"""
        if session_id:
            user = storage.find_user_by(session_id=session_id)
            return user if user else None
        return None

    def register_user(self, data: Dict) -> User:
        """register user based on email and password"""
        from models.cart import Cart
        user = storage.find_user_by(email=data['email'])
        if not user:
            user = storage.add_user(data)
            cart = Cart(user_id=user.id)
            cart.save()
            return user
        return None

    def valid_login(self, email: str, password: str) -> bool:
        """Check Valid login"""
        user = storage.find_user_by(email=email)
        # print("Valid", email, password)
        if user:
            if checkpw(password.encode(), user.password.encode()):
                return user
        return None

    def create_session(self, user: User) -> str:
        """Create session id using uuid"""
        storage.update_user(user, session_id=_generate_uuid())
        return user.session_id

    def destroy_session(self, user: User) -> None:
        """destroy session based on user id"""
        storage.update_user(user, session_id=None)
