"""
Authentication API endpoints.

Handles user registration and login.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.schemas.user import UserRegistration, UserLogin, UserResponse, AuthToken
from src.services.user_service import register_user, authenticate_user

# Create router
router = APIRouter()


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new user account with email and password.",
    responses={
        201: {
            "description": "User successfully registered",
            "content": {
                "application/json": {
                    "example": {
                        "user_id": "550e8400-e29b-41d4-a716-446655440000",
                        "email": "user@example.com",
                        "created_at": "2026-01-07T12:00:00Z",
                    }
                }
            },
        },
        400: {
            "description": "Email already exists",
            "content": {
                "application/json": {
                    "example": {"detail": "Email already exists"}
                }
            },
        },
    },
)
async def register(
    user_data: UserRegistration,
    db: AsyncSession = Depends(get_db),
) -> UserResponse:
    """
    Register a new user.

    **Request Body:**
    - email: Valid email address
    - password: Password (minimum 8 characters)

    **Returns:**
    - user_id: Unique user identifier
    - email: User's email address
    - created_at: Account creation timestamp

    **Example:**
    ```json
    {
        "email": "user@example.com",
        "password": "securePassword123"
    }
    ```
    """
    return await register_user(user_data, db)


@router.post(
    "/login",
    response_model=AuthToken,
    status_code=status.HTTP_200_OK,
    summary="Authenticate user and receive JWT token",
    description="Log in with email and password to receive an authentication token.",
    responses={
        200: {
            "description": "Authentication successful",
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "token_type": "bearer",
                        "user": {
                            "user_id": "550e8400-e29b-41d4-a716-446655440000",
                            "email": "user@example.com",
                            "created_at": "2026-01-07T12:00:00Z",
                        },
                    }
                }
            },
        },
        401: {
            "description": "Invalid credentials",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid email or password"}
                }
            },
        },
    },
)
async def login(
    login_data: UserLogin,
    db: AsyncSession = Depends(get_db),
) -> AuthToken:
    """
    Authenticate user and generate JWT token.

    **Request Body:**
    - email: User's registered email address
    - password: User's password

    **Returns:**
    - access_token: JWT token for authenticated requests
    - token_type: Always "bearer"
    - user: User information

    **Example:**
    ```json
    {
        "email": "user@example.com",
        "password": "securePassword123"
    }
    ```

    **Usage:**
    Use the returned `access_token` in subsequent requests:
    ```
    Authorization: Bearer <access_token>
    ```
    """
    return await authenticate_user(login_data, db)
