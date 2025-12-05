"""user_table

Revision ID: 49c16db0d32f
Revises: 
Create Date: 2025-11-19 00:11:06.187093

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '49c16db0d32f'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        'users',
        sa.Column('id', sa.Integer, autoincrement=True, primary_key=True),
        sa.Column('name', sa.Text, nullable=False),
        sa.Column('email', sa.Text, nullable=False, unique=True),
        sa.Column('password', sa.Text, nullable=False),
        sa.Column('avatar_url', sa.Text, nullable=True),
    )

    op.create_table(
        'sessions',
        sa.Column('id', sa.Integer, autoincrement=True, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey("users.id")),
        sa.Column('token', sa.Text, nullable=True),
        sa.Column('ip', sa.Text, nullable=True),
        sa.Column('user_agent', sa.Text, nullable=True),
        sa.Column('created_at', sa.Date, nullable=False, server_default=sa.func.now()),
    )


    pass


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_table('sessions')
    op.drop_table('users')

    pass
