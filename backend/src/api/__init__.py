"""
API routes module.

Contains all FastAPI routers for the application.
"""

from src.api import auth, tasks

__all__ = ["auth", "tasks"]
