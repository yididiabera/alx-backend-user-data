#!/usr/bin/env python3
"""Password related module"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Returns a hashed version of password"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Checks the validity of a password"""
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
