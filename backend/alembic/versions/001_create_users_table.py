"""Create users table

Revision ID: 001
Revises:
Create Date: 2026-01-07

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create users table with indexes."""
    op.create_table(
        'users',
        sa.Column('user_id', UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('email', sa.String(255), unique=True, nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )

    # Create index on email for fast login lookups
    op.create_index('idx_users_email', 'users', ['email'], unique=True)


def downgrade() -> None:
    """Drop users table and indexes."""
    op.drop_index('idx_users_email', table_name='users')
    op.drop_table('users')
