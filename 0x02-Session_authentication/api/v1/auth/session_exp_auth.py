#!//usr/bin/env python3
"""
handles session expiration
"""
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """
    Enhances session auth by adding expiry to Sessions
    """
    def __init__(self) -> None:
        """
        handle initialization
        """
        super().__init__()
        try:
            self.session_duration = int(getenv('SESSION_DURATION', 0))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        Creates a session for a logged in user
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        returns a user_id for a given session if it is not expired
        """
        if session_id is None:
            return None
        session_details: dict = self.user_id_by_session_id.get(session_id)
        if session_details is None:
            return None
        user_id = session_details.get('user_id')
        if self.session_duration <= 0:
            return user_id
        created_at = session_details.get('created_at')
        if created_at is None:
            return None
        validity_period = timedelta(seconds=self.session_duration)
        elapsed_time = datetime.now() - created_at
        if elapsed_time > validity_period:
            return None
        return user_id
