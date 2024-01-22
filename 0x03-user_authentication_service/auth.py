#!/usr/bin/env python3
"""
This module contains auth functionality
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """
    hashes a password string
    """
    pwd = password.encode('utf-8')
    hashed = bcrypt.hashpw(pwd, bcrypt.gensalt())
    return hashed
