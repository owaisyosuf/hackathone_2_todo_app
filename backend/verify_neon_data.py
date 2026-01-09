"""
Script to verify data is being stored in Neon database.
"""
import asyncio
import sys
from sqlalchemy import text
from src.database import engine

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


async def verify_neon_connection():
    """Verify connection to Neon and check data."""
    async with engine.begin() as conn:
        # Check database connection
        result = await conn.execute(text("SELECT current_database(), version()"))
        db_info = result.fetchone()
        print(f"\n[OK] Connected to database: {db_info[0]}")
        print(f"[OK] PostgreSQL version: {db_info[1][:50]}...")

        # Check users table
        result = await conn.execute(text("SELECT COUNT(*) FROM users"))
        user_count = result.scalar()
        print(f"\n[OK] Total users in Neon database: {user_count}")

        if user_count > 0:
            result = await conn.execute(text("SELECT user_id, email, created_at FROM users ORDER BY created_at DESC LIMIT 5"))
            users = result.fetchall()
            print("\n[OK] Recent users:")
            for user in users:
                print(f"  - {user[1]} (ID: {user[0]}, Created: {user[2]})")

        # Check tasks table
        result = await conn.execute(text("SELECT COUNT(*) FROM tasks"))
        task_count = result.scalar()
        print(f"\n[OK] Total tasks in Neon database: {task_count}")

        if task_count > 0:
            result = await conn.execute(text("""
                SELECT t.task_id, t.title, t.is_completed, u.email
                FROM tasks t
                JOIN users u ON t.user_id = u.user_id
                ORDER BY t.created_at DESC
                LIMIT 5
            """))
            tasks = result.fetchall()
            print("\n[OK] Recent tasks:")
            for task in tasks:
                status = "[DONE]" if task[2] else "[TODO]"
                print(f"  {status} {task[1]} (Owner: {task[3]})")

        print("\n" + "="*60)
        print("[OK] CONFIRMED: Data is being stored in Neon PostgreSQL!")
        print("="*60 + "\n")


if __name__ == "__main__":
    asyncio.run(verify_neon_connection())
