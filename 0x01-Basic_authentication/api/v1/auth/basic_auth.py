#!/usr/bin/env python3
"""
This module handles basic authentication
"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
    Handles Basic Auth
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        returns the Base64 part of the Authorization header for a
        Basic Authentication:
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        parts = authorization_header.split(' ')
        if parts[0] != 'Basic':
            return None
        return parts[1]
