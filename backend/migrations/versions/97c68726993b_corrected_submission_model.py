"""corrected submission model

Revision ID: 97c68726993b
Revises: 001d569a0be1
Create Date: 2024-02-20 19:37:34.404442

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "97c68726993b"
down_revision: Union[str, None] = "001d569a0be1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "submission",
        "is_correct",
        existing_type=sa.Boolean(),
        server_default=sa.text("false"),
    )
    op.alter_column(
        "submission",
        "points_awarded",
        existing_type=sa.Integer(),
        server_default=sa.text("0"),
    )


def downgrade() -> None:
    op.alter_column(
        "submission", "is_correct", existing_type=sa.Boolean(), server_default=None
    )
    op.alter_column(
        "submission", "points_awarded", existing_type=sa.Integer(), server_default=None
    )
