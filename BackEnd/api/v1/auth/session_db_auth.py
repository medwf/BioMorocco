#!/usr/bin/env python3
"""authentication module"""

# from models import storage
from models.engine.DBstorage import DBStorage
# from .auth import Auth
from bcrypt import hashpw, gensalt, checkpw
from models.user import User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from typing import List


def _hash_password(password: str) -> bytes:
    """methods that hashed password"""
    return hashpw(password.encode(), gensalt())


def _generate_uuid() -> str:
    """generate uuid based on uuid module"""
    from uuid import uuid4
    return str(uuid4())


class SessionDBAuth(DBStorage):
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        super().__init__()
        self.reload()

    def current_user(self, request=None):
        """return an instance based on cookie value"""
        if request is None:
            return None
        session_id = self.session_cookie(request)
        user = self.get_user_from_session_id(session_id)
        # user = self.get(User, 1)
        return user if user else None

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

    def authorization_header(self, request=None) -> str:
        """authorization header"""
        if request is None:
            return None
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None
        return auth_header

    def session_cookie(self, request=None):
        """Return a cookie value from a request"""
        if request is None:
            return None
        # nameCookie = getenv("SESSION_NAME", None)
        return request.cookies.get("session_id", None)

    def register_user(self, email: str, password: str) -> User:
        """register user based on email and password"""
        try:
            self.find_user_by(email=email)
        except (InvalidRequestError, NoResultFound):
            return self.add_user(email, _hash_password(password))
        raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """Check Valid login"""
        try:
            user = self.find_user_by(email=email)
            # print(user.email, user.password, type(user.password))
            if checkpw(password.encode(), user.password.encode()):
                return True
        except (InvalidRequestError, NoResultFound):
            return False
        return False

    def create_session(self, email: str) -> str:
        """Create session id using uuid"""
        try:
            user = self.find_user_by(email=email)
        except (InvalidRequestError, NoResultFound):
            return None
        user.session_id = _generate_uuid()
        self.update_user(user.id, session_id=user.session_id)
        return user.session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """get user based on session id"""
        if session_id:
            try:
                return self.find_user_by(session_id=session_id)
            except Exception:
                pass
        return None

    def destroy_session(self, user_id: str) -> None:
        """destroy session based on user id"""
        if not user_id:
            return None
        self.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """generate token"""
        try:
            user = self.find_user_by(email=email)
        except Exception:
            raise ValueError
        self.update_user(user.id, reset_token=_generate_uuid())
        return user.reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """update password"""
        try:
            user = self.find_user_by(reset_token=reset_token)
        except Exception:
            raise ValueError
        self.update_user(
            user.id,
            password=_hash_password(password),
            reset_token=None
        )
