"""Create tasks table

Revision ID: 002
Revises: 001
Create Date: 2026-01-07

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision: str = '002'
down_revision: Union[str, None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create tasks table with foreign key and indexes."""
    op.create_table(
        'tasks',
        sa.Column('task_id', UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('user_id', UUID(as_uuid=True),
                  sa.ForeignKey('users.user_id', ondelete='CASCADE'),
                  nullable=False),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_completed', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )

    # Create indexes for fast lookups
    op.create_index('idx_tasks_user_id', 'tasks', ['user_id'])
    op.create_index('idx_tasks_is_completed', 'tasks', ['is_completed'])


def downgrade() -> None:
    """Drop tasks table and indexes."""
    op.drop_index('idx_tasks_is_completed', table_name='tasks')
    op.drop_index('idx_tasks_user_id', table_name='tasks')
    op.drop_table('tasks')
