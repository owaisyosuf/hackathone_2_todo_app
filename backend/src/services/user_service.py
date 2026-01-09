"""
User service layer.

Handles user registration, authentication, and related business logic.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from src.models.user import User
from src.schemas.user import UserRegistration, UserLogin, UserResponse, AuthToken
from src.auth.password import hash_password, verify_password
from src.auth.jwt import create_access_token


async def register_user(
    user_data: UserRegistration,
    db: AsyncSession,
) -> UserResponse:
    """
    Register a new user.

    Args:
        user_data: User registration data (email, password)
        db: Database session

    Returns:
        UserResponse: Created user information

    Raises:
        HTTPException: 400 if email already exists

    Example:
        >>> user = await register_user(
        ...     UserRegistration(email="user@example.com", password="password123"),
        ...     db
        ... )
        >>> print(user.email)
        "user@example.com"
    """
    # Check if email already exists
    result = await db.execute(
        select(User).where(User.email == user_data.email)
    )
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists",
        )

    # Hash password
    hashed_password = hash_password(user_data.password)

    # Create new user
    new_user = User(
        email=user_data.email,
        password_hash=hashed_password,
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return UserResponse.model_validate(new_user)


async def authenticate_user(
    login_data: UserLogin,
    db: AsyncSession,
) -> AuthToken:
    """
    Authenticate a user and generate JWT token.

    Args:
        login_data: User login credentials (email, password)
        db: Database session

    Returns:
        AuthToken: JWT token and user information

    Raises:
        HTTPException: 401 if credentials are invalid

    Example:
        >>> auth_token = await authenticate_user(
        ...     UserLogin(email="user@example.com", password="password123"),
        ...     db
        ... )
        >>> print(auth_token.access_token)
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    """
    # Find user by email
    result = await db.execute(
        select(User).where(User.email == login_data.email)
    )
    user = result.scalar_one_or_none()

    # Verify user exists and password is correct
    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate JWT token
    access_token = create_access_token(
        user_id=str(user.user_id),
        email=user.email,
    )

    return AuthToken(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(user),
    )
