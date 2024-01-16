#!/usr/bin/env python3
"""
This module defines the auth class
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    Handles all API authentication issues
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        to implement
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        to implement
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        to implement
        """
        return None
