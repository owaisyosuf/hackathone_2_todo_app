"""
Authentication module.

Provides JWT token generation, validation, and password hashing utilities.
"""

from src.auth.jwt import create_access_token, verify_token, extract_user_id
from src.auth.password import hash_password, verify_password
from src.auth.middleware import get_current_user

__all__ = [
    "create_access_token",
    "verify_token",
    "extract_user_id",
    "hash_password",
    "verify_password",
    "get_current_user",
]
