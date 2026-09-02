"""add password reset fields

Revision ID: add_password_reset_fields
Revises: YOUR_PREVIOUS_REVISION
Create Date: 2026-09-02
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '032b23d273ba'
down_revision: Union[str, Sequence[str], None] = '032b23d273ab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    op.add_column(
        "users",
        sa.Column(
            "reset_token_hash",
            sa.String(length=64),
            nullable=True,
        ),
    )

    op.add_column(
        "users",
        sa.Column(
            "reset_token_expires_at",
            sa.DateTime(),
            nullable=True,
        ),
    )

    op.create_index(
        "ix_users_reset_token_hash",
        "users",
        ["reset_token_hash"],
        unique=False,
    )


def downgrade():

    op.drop_index(
        "ix_users_reset_token_hash",
        table_name="users",
    )

    op.drop_column(
        "users",
        "reset_token_expires_at",
    )

    op.drop_column(
        "users",
        "reset_token_hash",
    )