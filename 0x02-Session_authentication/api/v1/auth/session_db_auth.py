#!/usr/bin/env python3
"""A module for persistent session authentication"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime


class SessionDBAuth(SessionExpAuth):
    """A class for persistent session authentication"""
    def create_session(self, user_id=None):
        """Creates a session ID for a user_id"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Returns a user ID based on a session ID"""
        if session_id is None:
            return None
        user_session = UserSession.search({'session_id': session_id})
        if user_session is None:
            return None
        if self.session_duration <= 0:
            return user_session.user_id
        if user_session.created_at is None:
            return None
        if (user_session.created_at +
                self.session_duration < datetime.now()):
            return None
        return user_session.user_id

    def destroy_session(self, request=None):
        """Destroys the UserSession"""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_session = UserSession.search({'session_id': session_id})
        if len(user_session) == 0:
            return False
        user_session = user_session[0]
        user_session.remove()
        return True
