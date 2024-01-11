#!/usr/bin/env python3
"""
encryption module using bcrypt
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    encrypts a password using bcrypt and returns a salted, hashed password
    which is a byte string.
    """
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    validate that the provided password matches the hashed password
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
