#!/usr/bin/env python3
"""Authentication module"""
import re
import os
from flask import request
from typing import List, TypeVar, Union


class Auth:
    """Authentication class"""
    def require_auth(self, path: Union[str, None],
                     excluded_paths: List[str]) -> bool:
        """Determines if the path requires authentication"""
        if path and excluded_paths:
            for excluded in excluded_paths:
                pattern = ''
                if excluded[-1] == '*':
                    pattern = f'{excluded[0:-1]}.*'
                elif excluded[-1] == '/':
                    pattern = f'{excluded[0:-1]}/*'
                else:
                    pattern = f'{excluded}/*'
                if re.match(pattern, path):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """Returns None"""
        if request is None:
            return None
        if request.headers.get('Authorization'):
            return request.headers['Authorization']
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns None"""
        return None

    def session_cookie(self, request=None):
        """Returns a cookie value from a request"""
        if request is None:
            return None
        session_name = os.getenv('SESSION_NAME')
        return request.cookies.get(session_name)
