"""update tasks and attachments for ticket features

Revision ID: c4a4db57dfba
Revises: d10450d538f0
Create Date: 2026-08-13 13:17:16.259860

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


# revision identifiers, used by Alembic.
revision: str = "c4a4db57dfba"
down_revision: Union[str, Sequence[str], None] = "d10450d538f0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Add FileType to attachments
    op.add_column(
        "attachments",
        sa.Column(
            "FileType",
            sa.String(length=100),
            nullable=False
        )
    )

    # Add Base64 image data to attachments
    op.add_column(
        "attachments",
        sa.Column(
            "FileData",
            sa.Text(),
            nullable=False
        )
    )

    # Remove old file path column
    op.drop_column(
        "attachments",
        "FilePath"
    )

    # Allow tickets to be created without assigning a user.
    # A user can be assigned later using the assignment API.
    op.alter_column(
        "tasks",
        "AssignedTo",
        existing_type=mysql.INTEGER(),
        nullable=True
    )


def downgrade() -> None:
    """Downgrade schema."""

    # Make AssignedTo required again
    op.alter_column(
        "tasks",
        "AssignedTo",
        existing_type=mysql.INTEGER(),
        nullable=False
    )

    # Restore FilePath column
    op.add_column(
        "attachments",
        sa.Column(
            "FilePath",
            mysql.VARCHAR(length=500),
            nullable=False
        )
    )

    # Remove Base64 image data
    op.drop_column(
        "attachments",
        "FileData"
    )

    # Remove FileType
    op.drop_column(
        "attachments",
        "FileType"
    )