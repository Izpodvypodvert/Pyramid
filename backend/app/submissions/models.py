from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship


if TYPE_CHECKING:
    from app.steps.models import Step
    from app.users.models import User


class Submission(SQLModel, table=True):
    submission_id: int | None = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="user.user_id")
    step_id: int = Field(foreign_key="step.step_id")
    submitted_answer: str
    is_correct: bool
    points_awarded: int
    submitted_at: datetime

    step: "Step" = Relationship(back_populates="submissions")
    student: "User" = Relationship(back_populates="submissions")
