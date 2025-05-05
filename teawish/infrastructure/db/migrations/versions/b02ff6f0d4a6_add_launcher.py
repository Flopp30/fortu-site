"""add-launcher

Revision ID: b02ff6f0d4a6
Revises: f4ae321d7aaa
Create Date: 2025-05-03 12:24:36.947172

"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b02ff6f0d4a6'
down_revision: str | None = 'f4ae321d7aaa'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'launchers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('version', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('creator_id', sa.UUID(), nullable=False),
        sa.Column('file_path', sa.String(length=255), nullable=False),
        sa.ForeignKeyConstraint(['creator_id'], ['users.id'], name=op.f('fk_launchers_creator_id_users')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_launchers')),
        sa.UniqueConstraint('version', name=op.f('uq_launchers_version')),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('launchers')
