#!/usr/bin/env python3
"""
This module defines the auth class
"""
from flask import request
from typing import List, TypeVar
from os import getenv


class Auth:
    """
    Handles all API authentication issues
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        determines if a path is in the list of public paths - those
        requiring auth
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        for test_path in excluded_paths:
            if test_path[-1] == '*':
                if path.startswith(test_path[:-1]):
                    return False
            elif test_path.startswith(path):
                return False
        return not (path in excluded_paths)

    def authorization_header(self, request=None) -> str:
        """
        validate all requests to secure the API
        """
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        to implement
        """
        return None

    def session_cookie(self, request=None):
        """
        returns a cookie value from a request
        """
        if request is None:
            return None
        cookie_name = getenv('SESSION_NAME')
        return request.cookies.get(cookie_name)
