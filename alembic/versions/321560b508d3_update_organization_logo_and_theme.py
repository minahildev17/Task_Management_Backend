"""update organization logo and theme

Revision ID: 321560b508d3
Revises: d8edbb9aacdb
Create Date: 2026-08-04 12:38:50.871688

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "321560b508d3"
down_revision: Union[str, Sequence[str], None] = "d8edbb9aacdb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # LogoURL already exists in the database.
    # Keep the existing Theme column for now.
    # The Theme column will be replaced by ThemeID
    # in the next migration.

    op.drop_column(
        "organizations",
        "Logo"
    )


def downgrade() -> None:
    """Downgrade schema."""

    import sqlalchemy as sa

    op.add_column(
        "organizations",
        sa.Column(
            "Logo",
            sa.String(length=255),
            nullable=True
        )
    )