"""remove password reset fields

Revision ID: 032b23d273bc
Revises: 032b23d273ba
Create Date: 2026-09-02
"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "032b23d273bc"
down_revision: Union[str, Sequence[str], None] = "032b23d273ba"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
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


def downgrade():
    # This migration intentionally removes the obsolete
    # password-reset fields. Re-adding them is not required
    # for the current application.
    pass