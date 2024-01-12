from datetime import datetime
from typing import TYPE_CHECKING
from pydantic import UUID4

from sqlmodel import SQLModel, Field, Relationship


if TYPE_CHECKING:
    from app.steps.models import Step
    from app.users.models import User


class Submission(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    student_id: UUID4 = Field(foreign_key="user.id")
    step_id: int = Field(foreign_key="step.id")
    submitted_answer: str
    is_correct: bool
    points_awarded: int
    submitted_at: datetime

    step: "Step" = Relationship(back_populates="submissions")
    student: "User" = Relationship(back_populates="submissions")
