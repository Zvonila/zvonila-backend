"""chat_table

Revision ID: 0fe78afa075c
Revises: 49c16db0d32f
Create Date: 2025-11-19 00:12:56.495992

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0fe78afa075c'
down_revision: Union[str, Sequence[str], None] = '49c16db0d32f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "chats",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("initiator_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("receiver_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    pass


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_table("chats")
    
    pass
