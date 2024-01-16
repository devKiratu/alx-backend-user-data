#!/usr/bin/env python3
"""
This module defines the auth class
"""
from flask import request
from typing import List, TypeVar
import re


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
            if '*' in test_path:
                if re.match(test_path, path):
                    return False
        if path[-1] != '/':
            path += '/'
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
