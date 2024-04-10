"""added userprogress table

Revision ID: 43142ba622f1
Revises: 97c68726993b
Create Date: 2024-04-03 18:52:23.603979

"""

from typing import Sequence, Union

from alembic import op
import sqlmodel
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "43142ba622f1"
down_revision: Union[str, None] = "97c68726993b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "userprogress",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("course_id", sa.Integer(), nullable=True),
        sa.Column("lesson_id", sa.Integer(), nullable=True),
        sa.Column("step_id", sa.Integer(), nullable=True),
        sa.Column("is_completed", sa.Boolean(), nullable=False),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.Column(
            "progress_type",
            sa.Enum("STEP", "LESSON", "COURSE", name="progresstype"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["course_id"],
            ["course.id"],
        ),
        sa.ForeignKeyConstraint(
            ["lesson_id"],
            ["lesson.id"],
        ),
        sa.ForeignKeyConstraint(
            ["step_id"],
            ["step.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_userprogress_course_id"), "userprogress", ["course_id"], unique=False
    )
    op.create_index(
        op.f("ix_userprogress_lesson_id"), "userprogress", ["lesson_id"], unique=False
    )
    op.create_index(
        op.f("ix_userprogress_step_id"), "userprogress", ["step_id"], unique=False
    )
    op.add_column("step", sa.Column("course_id", sa.Integer(), nullable=False))
    op.create_foreign_key(None, "step", "course", ["course_id"], ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "step", type_="foreignkey")
    op.drop_column("step", "course_id")
    op.drop_index(op.f("ix_userprogress_step_id"), table_name="userprogress")
    op.drop_index(op.f("ix_userprogress_lesson_id"), table_name="userprogress")
    op.drop_index(op.f("ix_userprogress_course_id"), table_name="userprogress")
    op.drop_table("userprogress")
    # ### end Alembic commands ###