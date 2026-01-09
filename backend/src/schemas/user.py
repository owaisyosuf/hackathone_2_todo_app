"""
User Pydantic schemas for API validation.

These schemas define the structure for user-related API requests and responses.
"""

from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from uuid import UUID


class UserRegistration(BaseModel):
    """
    Schema for user registration request.

    Attributes:
        email: User's email address (must be valid email format)
        password: User's password (minimum 8 characters)
    """

    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=8, description="Password (min 8 characters)")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securePassword123",
            }
        }


class UserLogin(BaseModel):
    """
    Schema for user login request.

    Attributes:
        email: User's email address
        password: User's password
    """

    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., description="User's password")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securePassword123",
            }
        }


class UserResponse(BaseModel):
    """
    Schema for user data in API responses.

    Attributes:
        user_id: User's unique identifier
        email: User's email address
        created_at: Account creation timestamp
    """

    user_id: UUID = Field(..., description="User's unique identifier")
    email: EmailStr = Field(..., description="User's email address")
    created_at: datetime = Field(..., description="Account creation timestamp")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "user_id": "550e8400-e29b-41d4-a716-446655440000",
                "email": "user@example.com",
                "created_at": "2026-01-07T12:00:00Z",
            }
        }


class AuthToken(BaseModel):
    """
    Schema for authentication token response.

    Attributes:
        access_token: JWT access token
        token_type: Token type (always "bearer")
        user: User information
    """

    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    user: UserResponse = Field(..., description="Authenticated user information")

    class Config:
        json_schema_extra = {
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
