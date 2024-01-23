#!/usr/bin/env python3
"""
This module contains auth functionality
"""
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """
    hashes a password string
    """
    pwd = password.encode('utf-8')
    hashed = bcrypt.hashpw(pwd, bcrypt.gensalt())
    return hashed


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
            user = self._db.add_user(email, str(hashed_pwd))
            return user
