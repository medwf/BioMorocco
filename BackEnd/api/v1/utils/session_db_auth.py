#!/usr/bin/env python3
"""authentication module"""

# from models import storage
# from .auth import Auth
from bcrypt import checkpw
from models.user import User
from typing import List, Dict
from models import storage
from os import getenv

TIME_EXPIRATION = {
    'sec': 1,
    'min': 60,
    'hr': 60 * 60,
    "day": 60 * 60 * 24,
    "week": 60 * 60 * 24 * 7,
    "month": 60 * 60 * 24 * 7 * 4
}


def _generate_uuid() -> str:
    """generate uuid based on uuid module"""
    from uuid import uuid4
    return str(uuid4())


class SessionDBAuth():
    """Auth class to interact with the authentication database.
    """

    def require_auth(self, method: str, path: str, excluded_paths: List[str]) -> bool:
        """require auth"""
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        if method == 'GET' and (('categories' in path) or ('products' in path)):
            return False
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
        from api.v1.app import redis_client

        if request is None:
            return None
        session_id = self.session_cookie(request)
        if not session_id:
            return None
        user_id = redis_client.get(f"auth_{session_id}")
        user = storage.get(User, user_id)
        return user if user else None

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
        if user:
            if checkpw(password.encode(), user.password.encode()):
                return user
        return None

    def create_session(self, user: User) -> str:
        """Create session id using uuid"""
        # storage.update(user, session_id=_generate_uuid())
        from api.v1.app import redis_client

        session_id = _generate_uuid()

        get_exp = getenv("SESSION_EXP", "1-day")
        multi, time = get_exp.split("-")
        duration = TIME_EXPIRATION[time] * int(multi)

        redis_client.set(
            f"auth_{session_id}",
            user.id,
            duration
        )
        return session_id

    @staticmethod
    def create_code_for_reset_password(user_id):
        """create code by define expiration 2m"""
        from random import randint
        from api.v1.app import redis_client

        code = randint(100000, 999999)

        get_exp = getenv('REST_PASSWORD_EXP', '2-min')
        multi, time = get_exp.split("-")
        print(multi, time)
        duration = TIME_EXPIRATION[time] * int(multi)
        print(TIME_EXPIRATION[time])
        print(duration)

        redis_client.set(
            f"code_{code}",
            user_id,
            duration
        )
        print(code)
        return code

    @staticmethod
    def check_code_for_reset_password(code):
        """check user_id based on code"""
        from api.v1.app import redis_client

        user_id = redis_client.get(f"code_{code}")
        if user_id:
            redis_client.delete(f"code_{code}")
        user = storage.get(User, user_id)
        return user if user else None

    def destroy_session(self) -> None:
        """destroy session based on user id"""
        # storage.update(user, session_id=None)
        from flask import request
        from api.v1.app import redis_client

        session_id = self.session_cookie(request)
        redis_client.delete(f"auth_{session_id}")
