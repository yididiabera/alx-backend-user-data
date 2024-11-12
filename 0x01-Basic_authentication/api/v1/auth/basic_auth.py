#!/usr/bin/env python3
"""Basic auth implementation method"""
import base64
import re
from api.v1.auth.auth import Auth
from models.user import User
from typing import Union, Tuple, TypeVar


class BasicAuth(Auth):
    """Basic Auth implementation class"""
    def extract_base64_authorization_header(self,
                                            authorization_header:
                                            str) -> Union[
                                                 str, None]:
        """Returns base64 part of authorization header"""
        if authorization_header is None:
            return None
        if not type(authorization_header) == str:
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """Decodes the base64 authorization header"""
        if base64_authorization_header is None:
            return None
        if not type(base64_authorization_header) == str:
            return None
        try:
            decoded = base64.b64decode(base64_authorization_header)
            value = decoded.decode('utf-8')
            return value
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> Tuple[str, str]:
        """Returns user email and password from decoded base64"""
        if type(decoded_base64_authorization_header) == str:
            pattern = re.compile(r'(?P<email>[^:]+):(?P<password>.+)')
            credentials = pattern.match(
                decoded_base64_authorization_header.strip())
            if credentials:
                email = credentials.group('email')
                password = credentials.group('password')
                return email, password
        return None, None

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """Returns a user instance based on email and password"""
        if user_email is None or type(user_email) != str:
            return None
        if user_pwd is None or type(user_pwd) != str:
            return None
        attributes = {'email': user_email}
        try:
            user_list = User.search(attributes)
        except Exception:
            return None
        if len(user_list) <= 0:
            return None
        if user_list[0].is_valid_password(user_pwd):
            return user_list[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns the current user instance"""
        auth_header = self.authorization_header(request)
        base64_header = self.extract_base64_authorization_header(auth_header)
        decoded = self.decode_base64_authorization_header(base64_header)
        email, password = self.extract_user_credentials(decoded)
        user = self.user_object_from_credentials(email, password)
        return user
