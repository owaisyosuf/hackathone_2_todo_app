"""
Application configuration management.

Loads environment variables and provides typed configuration settings.
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """

    # Database
    DATABASE_URL: str

    # JWT Authentication
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 60

    # Application
    ENVIRONMENT: str = "development"
    API_TITLE: str = "Todo Application API"
    API_VERSION: str = "2.0.0"

    # CORS
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:8000"

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
