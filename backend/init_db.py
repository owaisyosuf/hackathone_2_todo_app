"""
Initialize database tables.
Run this script to create all database tables.
"""

import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from src.config import settings
from src.database import Base

# Import all models to ensure they're registered with Base
from src.models.user import User
from src.models.task import Task
from src.models.chat import Conversation, ChatMessage


async def init_db():
    """Create all database tables."""
    print(f"Connecting to database: {settings.DATABASE_URL[:50]}...")

    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=True,
    )

    async with engine.begin() as conn:
        print("Creating all tables...")
        await conn.run_sync(Base.metadata.create_all)

    await engine.dispose()
    print("✅ Database initialized successfully!")


if __name__ == "__main__":
    asyncio.run(init_db())
