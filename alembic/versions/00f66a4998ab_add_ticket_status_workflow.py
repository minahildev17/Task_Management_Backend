"""add ticket status workflow

Revision ID: 00f66a4998ab
Revises: 761e9c24b40d
Create Date: 2026-08-18 16:23:44.229564

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


# revision identifiers, used by Alembic.
revision: str = '00f66a4998ab'
down_revision: Union[str, Sequence[str], None] = '761e9c24b40d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Convert existing Pending statuses to Ready to Do
    op.execute(
        "UPDATE tasks SET `Status` = 'READY_TO_DO' WHERE `Status` = 'Pending'"
    )

    # Change Status column from VARCHAR to Enum
    op.alter_column(
        'tasks',
        'Status',
        existing_type=mysql.VARCHAR(length=50),
        type_=sa.Enum(
            'READY_TO_DO',
            'IN_PROGRESS',
            'BLOCKED',
            'TESTING',
            'DONE',
            name='taskstatus'
        ),
        existing_nullable=False
    )


def downgrade() -> None:
    """Downgrade schema."""

    # Convert Ready to Do back to Pending before changing the column type
    op.execute(
        "UPDATE tasks SET `Status` = 'Pending' WHERE `Status` = 'READY_TO_DO'"
    )

    # Change Status column back to VARCHAR
    op.alter_column(
        'tasks',
        'Status',
        existing_type=sa.Enum(
            'READY_TO_DO',
            'IN_PROGRESS',
            'BLOCKED',
            'TESTING',
            'DONE',
            name='taskstatus'
        ),
        type_=mysql.VARCHAR(length=50),
        existing_nullable=False
    )