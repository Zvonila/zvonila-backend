"""call table

Revision ID: edc0fb381d38
Revises: a2e8ece8e933
Create Date: 2025-12-06 23:52:15.639056

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'edc0fb381d38'
down_revision: Union[str, Sequence[str], None] = 'a2e8ece8e933'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    call_type_enum = postgresql.ENUM('audio', 'video', name='call_type', create_type=False)
    call_status_enum = postgresql.ENUM('ringing', 'accepted', 'canceled', 'declined', 'timeout', 'ended',
                                       name='call_status', create_type=False)
    participant_role_enum = postgresql.ENUM('initiator', 'peer', name='participant_role', create_type=False)
    participant_status_enum = postgresql.ENUM(
        'ringing', 'notified', 'accepted', 'rejected', 'disconnected',
        name='participant_status', create_type=False
    )

    call_type_enum.create(op.get_bind(), checkfirst=True)
    call_status_enum.create(op.get_bind(), checkfirst=True)
    participant_role_enum.create(op.get_bind(), checkfirst=True)
    participant_status_enum.create(op.get_bind(), checkfirst=True)

    # TABLE: calls
    op.create_table(
        'calls',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('initiator_id', sa.Integer, nullable=False),
        sa.Column('type', call_type_enum, nullable=False),
        sa.Column('status', call_status_enum, nullable=False, server_default="ringing"),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('answered_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('ended_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_update_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['initiator_id'], ['users.id'], ondelete='CASCADE'),
    )

    # TABLE: call_participants
    op.create_table(
        'call_participants',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('call_id', sa.Integer, nullable=False),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('role', participant_role_enum, nullable=False),
        sa.Column('status', participant_status_enum, nullable=False, server_default="ringing"),
        sa.Column('joined_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('left_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['call_id'], ['calls.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('call_id', 'user_id', name='uq_call_user')
    )

    pass


def downgrade() -> None:
    """Downgrade schema."""
    
    op.drop_table('call_participants')
    op.drop_table('calls')

    # drop enums
    op.execute('DROP TYPE IF EXISTS participant_status')
    op.execute('DROP TYPE IF EXISTS participant_role')
    op.execute('DROP TYPE IF EXISTS call_status')
    op.execute('DROP TYPE IF EXISTS call_type')

    pass
