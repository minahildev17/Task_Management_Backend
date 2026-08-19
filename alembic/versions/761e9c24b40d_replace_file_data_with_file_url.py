"""replace file data with file url

Revision ID: 761e9c24b40d
Revises: c4a4db57dfba
Create Date: 2026-08-18 13:42:16.211046

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '761e9c24b40d'
down_revision: Union[str, Sequence[str], None] = 'c4a4db57dfba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Remove old Base64 image storage column
    op.drop_column('attachments', 'FileData')

    # Add MinIO image URL column
    op.add_column(
        'attachments',
        sa.Column('FileURL', sa.String(length=500), nullable=True)
    )


def downgrade() -> None:
    """Downgrade schema."""

    # Remove MinIO URL column
    op.drop_column('attachments', 'FileURL')

    # Restore old Base64 image storage column
    op.add_column(
        'attachments',
        sa.Column('FileData', sa.Text(), nullable=True)
    )