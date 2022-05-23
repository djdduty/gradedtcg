"""main tables

Revision ID: fdf8821871d7
Revises:
Create Date: 2019-09-22 01:36:44.791880

"""
from typing import Tuple

import sqlalchemy as sa
import uuid
from alembic import op
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID

revision = "fdf8821871d7"
down_revision = None
branch_labels = None
depends_on = None


def create_updated_at_trigger() -> None:
    op.execute(
        """
    CREATE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS
    $$
    BEGIN
        NEW.updated_at = now();
        RETURN NEW;
    END;
    $$ language 'plpgsql';
    """
    )


def timestamps() -> Tuple[sa.Column, sa.Column]:
    return (
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=func.now(),
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=func.now(),
            onupdate=func.current_timestamp(),
        ),
    )


def create_users_table() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("username", sa.Text, unique=True, nullable=False, index=True),
        sa.Column("email", sa.Text, unique=True, nullable=False, index=True),
        sa.Column("salt", sa.Text, nullable=False),
        sa.Column("hashed_password", sa.Text),
        sa.Column("bio", sa.Text, nullable=False, server_default=""),
        sa.Column("image", sa.Text),
        *timestamps(),
    )
    op.execute(
        """
        CREATE TRIGGER update_user_modtime
            BEFORE UPDATE
            ON users
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """
    )


def create_tcgs_table() -> None:
    op.create_table(
        "tcgs",
        sa.Column("name_en", sa.Text, primary_key=True),
        *timestamps(),
    )
    op.execute(
        """
        CREATE TRIGGER update_tcgs_modtime
            BEFORE UPDATE
            ON tcgs
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """
    )


def create_sets_table() -> None:
    op.create_table(
        "sets",
        sa.Column("uuid", UUID(as_uuid=True), primary_key=True, unique=True, nullable=False),
        sa.Column("tcg_id", sa.Text, sa.ForeignKey("tcgs.name_en", ondelete="CASCADE"), nullable=False),
        sa.Column("code", sa.Text, nullable=False, unique=True, index=True),
        *timestamps(),
    )
    op.execute(
        """
        CREATE TRIGGER update_sets_modtime
            BEFORE UPDATE
            ON sets
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """
    )


def create_cards_table() -> None:
    op.create_table(
        "cards",
        sa.Column("uuid", UUID(as_uuid=True), primary_key=True, unique=True, nullable=False),
        sa.Column("tcg_id", sa.Text, sa.ForeignKey("tcgs.name_en", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("set_id", UUID(as_uuid=True), sa.ForeignKey("sets.uuid", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("collector_number", sa.Integer, nullable=False, index=True),
        sa.Column("name_en", sa.Text, primary_key=True),
        *timestamps(),
    )
    op.execute(
        """
        CREATE TRIGGER update_cards_modtime
            BEFORE UPDATE
            ON cards
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """
    )


def create_collectibles_table() -> None:
    op.create_table(
        "collectibles",
        sa.Column("id", sa.Integer, nullable=False),
        sa.Column("owner_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("uuid", UUID(as_uuid=True), default=uuid.uuid4, index=True, nullable=False),
        sa.Column("is_card", sa.Boolean, nullable=False),
        sa.Column("is_graded", sa.Boolean, nullable=False),
        sa.Column("is_shared", sa.Boolean, nullable=False, default=False),

        # Sealed product meta
        sa.Column("name", sa.Text),
        sa.Column("description", sa.Text),

        # Card common meta
        sa.Column("card_id", UUID(as_uuid=True), sa.ForeignKey("cards.uuid", ondelete="SET NULL"), index=True, nullable=True, unique=False),
        sa.Column("set_id", UUID(as_uuid=True), sa.ForeignKey("sets.uuid", ondelete="SET NULL"), index=True, nullable=True, unique=False),
        
        # Ungraded meta
        sa.Column("quantity", sa.Integer, default=1, nullable=False),

        # Graded meta
        sa.Column("grade_overall", sa.Numeric(3, 1), nullable=True),
        sa.Column("grade_centering", sa.Numeric(3, 1), nullable=True),
        sa.Column("grade_corners", sa.Numeric(3, 1), nullable=True),
        sa.Column("grade_edges", sa.Numeric(3, 1), nullable=True),
        sa.Column("grade_surface", sa.Numeric(3, 1), nullable=True),
        sa.Column("grade_signature", sa.Numeric(3, 1), nullable=True),
        sa.Column("grade_org", sa.Text, nullable=True),
        sa.Column("grade_serial_no", sa.Text, nullable=True),

        # Timestamps
        *timestamps(),
    )
    op.create_primary_key(
        "pk_collectibles", "collectibles", ["id", "owner_id"]
    )
    op.execute(
        """
        ALTER TABLE collectibles
        ADD CONSTRAINT chk_grade_overall CHECK (grade_overall >= 0 and grade_overall <= 10);
        """
    )
    op.execute(
        """
        ALTER TABLE collectibles
        ADD CONSTRAINT chk_grade_centering CHECK (grade_centering >= 0 and grade_centering <= 10);
        """
    )
    op.execute(
        """
        ALTER TABLE collectibles
        ADD CONSTRAINT chk_grade_corners CHECK (grade_corners >= 0 and grade_corners <= 10);
        """
    )
    op.execute(
        """
        ALTER TABLE collectibles
        ADD CONSTRAINT chk_grade_edges CHECK (grade_edges >= 0 and grade_edges <= 10);
        """
    )
    op.execute(
        """
        ALTER TABLE collectibles
        ADD CONSTRAINT chk_grade_surface CHECK (grade_surface >= 0 and grade_surface <= 10);
        """
    )
    op.execute(
        """
        ALTER TABLE collectibles
        ADD CONSTRAINT chk_grade_signature CHECK (grade_signature >= 0 and grade_signature <= 10);
        """
    )
    op.execute(
        """
        ALTER TABLE collectibles
        ADD CONSTRAINT chk_grade_org CHECK (grade_org IN ('BGS', 'PSA'));
        """
    )
    op.execute(
        """
        ALTER TABLE collectibles
        ADD CONSTRAINT chk_collectible_card_meta CHECK (
            (is_card = true and card_id IS NOT NULL and set_id IS NOT NULL)
            or
            (is_card = false and card_id IS NULL and set_id IS NULL)
        );
        """
    )
    op.execute(
        """
        ALTER TABLE collectibles
        ADD CONSTRAINT chk_collectible_graded_meta CHECK (
            (is_graded = true and grade_overall IS NOT NULL and grade_centering IS NOT NULL and grade_corners IS NOT NULL and grade_edges IS NOT NULL and grade_surface IS NOT NULL and grade_serial_no IS NOT NULL)
            or
            (is_graded = false and grade_overall IS NULL and grade_centering IS NULL and grade_corners IS NULL and grade_edges IS NULL and grade_surface IS NULL and grade_serial_no IS NULL)
        );
        """
    )
    op.execute(
        """
        CREATE TRIGGER update_collectibles_modtime
            BEFORE UPDATE
            ON collectibles
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """
    )


def upgrade() -> None:
    create_updated_at_trigger()
    create_users_table()
    create_tcgs_table()
    create_sets_table()
    create_cards_table()
    create_collectibles_table()


def downgrade() -> None:
    op.drop_table("collectibles")
    op.drop_table("cards")
    op.drop_table("sets")
    op.drop_table("tcgs")
    op.drop_table("users")
    op.execute("DROP FUNCTION update_updated_at_column")
