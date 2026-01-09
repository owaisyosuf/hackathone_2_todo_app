"""
JWT token generation and validation.

Uses Better Auth SDK for secure JWT token management.
"""

from datetime import datetime, timedelta
from typing import Dict, Optional
import jwt
from jwt.exceptions import InvalidTokenError

from src.config import settings


def create_access_token(user_id: str, email: str) -> str:
    """
    Generate a JWT access token for an authenticated user.

    Args:
        user_id: User's unique identifier (UUID as string)
        email: User's email address

    Returns:
        str: Encoded JWT token

    Example:
        >>> token = create_access_token("user-uuid", "user@example.com")
        >>> print(token)
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    """
    expiration = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRATION_MINUTES)

    payload = {
        "sub": user_id,  # Subject (user ID)
        "email": email,
        "exp": expiration,  # Expiration time
        "iat": datetime.utcnow(),  # Issued at
        "type": "access",
    }

    token = jwt.encode(
        payload,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM,
    )

    return token


def verify_token(token: str) -> Optional[Dict]:
    """
    Validate and decode a JWT token.

    Args:
        token: JWT token string

    Returns:
        Optional[Dict]: Decoded token payload if valid, None if invalid

    Example:
        >>> payload = verify_token("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
        >>> print(payload["sub"])  # User ID
        "user-uuid"
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
        )

        # Verify token type
        if payload.get("type") != "access":
            return None

        return payload

    except InvalidTokenError:
        return None
    except Exception:
        return None


def extract_user_id(token: str) -> Optional[str]:
    """
    Extract user ID from a JWT token.

    Args:
        token: JWT token string

    Returns:
        Optional[str]: User ID if token is valid, None otherwise

    Example:
        >>> user_id = extract_user_id("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
        >>> print(user_id)
        "user-uuid"
    """
    payload = verify_token(token)
    if payload:
        return payload.get("sub")
    return None
