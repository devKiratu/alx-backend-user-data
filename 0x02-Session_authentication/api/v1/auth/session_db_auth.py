#!/usr/bin/env python3
"""
Defines session auth module with db support
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from models.user import User
from datetime import datetime, timedelta
import uuid


class SessionDBAuth(SessionExpAuth):
    """
    Extends Session Authentication with expiry to save session
    details in the db
    """
    def create_session(self, user_id=None):
        """
        creates and stores new instance of UserSession and returns the
        Session ID
        """
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        user_session = UserSession()
        user_session.created_at = datetime.now()
        user_session.session_id = session_id
        user_session.user_id = user_id
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        returns the User ID by requesting UserSession in the database
        based on session_id
        """
        if session_id is None:
            return None
        try:
            user_session_data = UserSession.search({'session_id': session_id})
            if len(user_session_data) == 0:
                return None
            user_session: UserSession = user_session_data[0]
            user_id = user_session.user_id
            if self.session_duration <= 0:
                return user_id
            created_at = user_session.created_at
            if created_at is None:
                return None
            validity_period = timedelta(seconds=self.session_duration)
            elapsed_time = datetime.now() - created_at
            if elapsed_time > validity_period:
                return None
            return user_id
        except Exception:
            return None

    def destroy_session(self, request=None):
        """
        destroys the UserSession based on the Session ID from the
        request cookie
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_session_data = UserSession.search({'session_id': session_id})
        if len(user_session_data) == 0:
            return None
        user_session: UserSession = user_session_data[0]
        user_session.remove()
        return True

    def current_user(self, request=None):
        """
        returns a User instance based on a cookie value
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        user = User.get(user_id)
        return user
