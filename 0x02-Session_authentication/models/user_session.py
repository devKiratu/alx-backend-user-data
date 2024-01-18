#!/usr/bin/env python3
"""
Extends User model by adding session details
"""
from models.base import Base


class UserSession(Base):
    """
    User class with session data
    """
    def __init__(self, *args: list, **kwargs: dict):
        """initiaize the user object"""
        super().__init__(*args, **kwargs)
        self.user_id = ""
        self.session_id = ""
