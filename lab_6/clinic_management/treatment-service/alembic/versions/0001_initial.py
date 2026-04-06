"""Initial migration — diagnoses and prescriptions.

Revision ID: 0001
Revises:
Create Date: 2026-03-30

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "diagnoses",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("visit_id", sa.Integer(), unique=True, nullable=False),
        sa.Column("icd_code", sa.String(10), nullable=False),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("description", sa.String(1000), nullable=True),
        sa.Column(
            "severity",
            sa.Enum("MILD", "MODERATE", "SEVERE", name="diagnosis_severity"),
            nullable=False,
        ),
        sa.Column(
            "diagnosed_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )

    op.create_table(
        "prescriptions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "diagnosis_id",
            sa.Integer(),
            sa.ForeignKey("diagnoses.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("medication_name", sa.String(200), nullable=False),
        sa.Column("dosage", sa.String(100), nullable=False),
        sa.Column("frequency", sa.String(100), nullable=False),
        sa.Column("duration_days", sa.Integer(), nullable=False),
        sa.Column("cost", sa.Numeric(10, 2), nullable=False),
        sa.Column("notes", sa.String(1000), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_table("prescriptions")
    op.drop_table("diagnoses")
    op.execute("DROP TYPE diagnosis_severity;")
