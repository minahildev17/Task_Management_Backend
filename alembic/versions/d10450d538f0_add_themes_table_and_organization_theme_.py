"""add themes table and organization theme foreign key

Revision ID: d10450d538f0
Revises: 321560b508d3
Create Date: 2026-08-12 16:21:41.917292

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d10450d538f0"
down_revision: Union[str, Sequence[str], None] = "321560b508d3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    bind = op.get_bind()
    inspector = sa.inspect(bind)

    # ---------------------------------------------------------
    # 1. Create themes table if it does not already exist
    # ---------------------------------------------------------

    tables = inspector.get_table_names()

    if "themes" not in tables:
        op.create_table(
            "themes",
            sa.Column("ThemeID", sa.Integer(), nullable=False),
            sa.Column("Name", sa.String(length=50), nullable=False),
            sa.PrimaryKeyConstraint("ThemeID"),
            sa.UniqueConstraint("Name")
        )

        op.create_index(
            "ix_themes_ThemeID",
            "themes",
            ["ThemeID"],
            unique=False
        )

    # ---------------------------------------------------------
    # 2. Insert default themes
    # ---------------------------------------------------------

    op.execute(
        """
        INSERT INTO themes (ThemeID, Name)
        VALUES
            (1, 'light'),
            (2, 'dark'),
            (3, 'blue'),
            (4, 'green')
        ON DUPLICATE KEY UPDATE
            Name = VALUES(Name)
        """
    )

    # Refresh inspector after possible schema changes
    inspector = sa.inspect(bind)

    # ---------------------------------------------------------
    # 3. Add ThemeID only if it does not already exist
    # ---------------------------------------------------------

    organization_columns = {
        column["name"]
        for column in inspector.get_columns("organizations")
    }

    if "ThemeID" not in organization_columns:
        op.add_column(
            "organizations",
            sa.Column(
                "ThemeID",
                sa.Integer(),
                nullable=True
            )
        )

    # ---------------------------------------------------------
    # 4. Convert old Theme values to ThemeID
    # ---------------------------------------------------------

    inspector = sa.inspect(bind)

    organization_columns = {
        column["name"]
        for column in inspector.get_columns("organizations")
    }

    if "Theme" in organization_columns:
        op.execute(
            """
            UPDATE organizations
            SET ThemeID =
                CASE LOWER(Theme)
                    WHEN 'light' THEN 1
                    WHEN 'dark' THEN 2
                    WHEN 'blue' THEN 3
                    WHEN 'green' THEN 4
                    ELSE 1
                END
            """
        )

    else:
        # If the old Theme column is already gone,
        # make sure any NULL ThemeID gets the default theme.
        op.execute(
            """
            UPDATE organizations
            SET ThemeID = 1
            WHERE ThemeID IS NULL
            """
        )

    # ---------------------------------------------------------
    # 5. Make ThemeID NOT NULL
    # ---------------------------------------------------------

    op.alter_column(
        "organizations",
        "ThemeID",
        existing_type=sa.Integer(),
        nullable=False
    )

    # ---------------------------------------------------------
    # 6. Add foreign key only if it does not already exist
    # ---------------------------------------------------------

    inspector = sa.inspect(bind)

    foreign_keys = inspector.get_foreign_keys("organizations")

    theme_fk_exists = any(
        fk.get("referred_table") == "themes"
        and fk.get("constrained_columns") == ["ThemeID"]
        for fk in foreign_keys
    )

    if not theme_fk_exists:
        op.create_foreign_key(
            "fk_organizations_theme",
            "organizations",
            "themes",
            ["ThemeID"],
            ["ThemeID"]
        )

    # ---------------------------------------------------------
    # 7. Remove old Theme column if it still exists
    # ---------------------------------------------------------

    inspector = sa.inspect(bind)

    organization_columns = {
        column["name"]
        for column in inspector.get_columns("organizations")
    }

    if "Theme" in organization_columns:
        op.drop_column(
            "organizations",
            "Theme"
        )


def downgrade() -> None:
    """Downgrade schema."""

    bind = op.get_bind()
    inspector = sa.inspect(bind)

    # ---------------------------------------------------------
    # 1. Add old Theme column if it does not exist
    # ---------------------------------------------------------

    organization_columns = {
        column["name"]
        for column in inspector.get_columns("organizations")
    }

    if "Theme" not in organization_columns:
        op.add_column(
            "organizations",
            sa.Column(
                "Theme",
                sa.String(length=100),
                nullable=True
            )
        )

    # ---------------------------------------------------------
    # 2. Restore old Theme values
    # ---------------------------------------------------------

    op.execute(
        """
        UPDATE organizations o
        JOIN themes t ON o.ThemeID = t.ThemeID
        SET o.Theme = t.Name
        """
    )

    # ---------------------------------------------------------
    # 3. Remove foreign key
    # ---------------------------------------------------------

    inspector = sa.inspect(bind)

    foreign_keys = inspector.get_foreign_keys("organizations")

    for fk in foreign_keys:
        if (
            fk.get("referred_table") == "themes"
            and fk.get("constrained_columns") == ["ThemeID"]
        ):
            constraint_name = fk.get("name")

            if constraint_name:
                op.drop_constraint(
                    constraint_name,
                    "organizations",
                    type_="foreignkey"
                )

    # ---------------------------------------------------------
    # 4. Remove ThemeID
    # ---------------------------------------------------------

    inspector = sa.inspect(bind)

    organization_columns = {
        column["name"]
        for column in inspector.get_columns("organizations")
    }

    if "ThemeID" in organization_columns:
        op.drop_column(
            "organizations",
            "ThemeID"
        )

    # ---------------------------------------------------------
    # 5. Drop themes table
    # ---------------------------------------------------------

    inspector = sa.inspect(bind)

    if "themes" in inspector.get_table_names():
        indexes = inspector.get_indexes("themes")

        for index in indexes:
            if index["name"] == "ix_themes_ThemeID":
                op.drop_index(
                    "ix_themes_ThemeID",
                    table_name="themes"
                )

        op.drop_table("themes")