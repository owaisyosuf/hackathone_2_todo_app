"""
Password hashing utilities.

Provides secure password hashing and verification using bcrypt.
"""

from passlib.context import CryptContext
import bcrypt

# Configure password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def safe_hash_password(password: str) -> str:
    """
    Safely hash a password using bcrypt with 72-character limit handling.

    Args:
        password: Plain text password

    Returns:
        str: Hashed password
    """
    # Ensure password is not too long for bcrypt (72 character limit)
    if len(password) > 72:
        password = password[:72]

    # Convert to bytes if it's a string
    if isinstance(password, str):
        password_bytes = password.encode('utf-8')
    else:
        password_bytes = password

    # Use bcrypt directly to avoid passlib issues
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)

    # Convert back to string
    return hashed.decode('utf-8')


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.

    Args:
        password: Plain text password

    Returns:
        str: Hashed password

    Example:
        >>> hashed = hash_password("mypassword123")
        >>> print(hashed)
        "$2b$12$..."
    """
    # Bcrypt has a 72 character limit, so we truncate if necessary
    if len(password) > 72:
        password = password[:72]

    # Additional safety check to ensure password is not empty after truncation
    if not password:
        raise ValueError("Password cannot be empty")

    try:
        return pwd_context.hash(password)
    except Exception as e:
        # If passlib fails (e.g., due to bcrypt limitations), use direct bcrypt
        import bcrypt
        if len(password) > 72:
            password = password[:72]

        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hashed password.

    Args:
        plain_password: Plain text password to verify
        hashed_password: Hashed password to compare against

    Returns:
        bool: True if password matches, False otherwise

    Example:
        >>> hashed = hash_password("mypassword123")
        >>> verify_password("mypassword123", hashed)
        True
        >>> verify_password("wrongpassword", hashed)
        False
    """
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        # If verification fails due to bcrypt limitations, handle gracefully
        import bcrypt
        if len(plain_password) > 72:
            plain_password = plain_password[:72]

        plain_password_bytes = plain_password.encode('utf-8')
        hashed_password_bytes = hashed_password.encode('utf-8') if isinstance(hashed_password, str) else hashed_password

        return bcrypt.checkpw(plain_password_bytes, hashed_password_bytes)
