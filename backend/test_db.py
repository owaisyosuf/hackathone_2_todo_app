import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from src.config import settings

async def test_db_connection():
    print("Testing database connection...")
    print(f"Database URL: {settings.DATABASE_URL}")

    try:
        engine = create_async_engine(settings.DATABASE_URL, echo=True)

        async with engine.connect() as conn:
            print("Connection successful!")
            result = await conn.execute("SELECT 1")
            print(f"Query result: {result.fetchone()}")

        await engine.dispose()
        print("Engine disposed successfully!")

    except Exception as e:
        print(f"Error connecting to database: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_db_connection())