#!/usr/bin/env python3
"""
This module contains auth functionality
"""
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
import uuid
from typing import Union
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """
    hashes a password string
    """
    pwd = password.encode('utf-8')
    hashed = bcrypt.hashpw(pwd, bcrypt.gensalt())
    return hashed


def _generate_uuid() -> str:
    """
    return a string representation of a new UUID
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """
    def __init__(self):
        """
        init db class
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        registers a new user
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            hashed_pwd = _hash_password(password)
            user = self._db.add_user(email, hashed_pwd)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validates login credentials
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password)
        except NoResultFound:
            return False
        except InvalidRequestError:
            return False

    def create_session(self, email: str) -> str:
        """
        creates and returns a user session
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user_id=user.id, session_id=session_id)
            return session_id
        except Exception:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """
        retrieves a user using session_id
        """
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except Exception:
            return None
