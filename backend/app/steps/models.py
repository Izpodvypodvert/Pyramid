from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship
from enum import Enum


if TYPE_CHECKING:
    from app.courses.models import Lesson
    from app.submissions.models import Submission


class StepKind(Enum):
    THEORY = "Theory"
    CODING_TASK = "CodingTask"
    TEST = "Test"


class TestType(Enum):
    SIMPLE = "Simple"
    ADVANCED = "Advanced"


class Step(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    lesson_id: int = Field(foreign_key="lesson.id")
    order: int
    step_kind: StepKind
    is_published: bool = False

    lesson: "Lesson" = Relationship(back_populates="steps")
    theories: list["Theory"] = Relationship(back_populates="step")
    coding_tasks: list["CodingTask"] = Relationship(back_populates="step")
    tests: list["Test"] = Relationship(back_populates="step")
    submissions: list["Submission"] = Relationship(back_populates="step")


class Theory(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    step_id: int = Field(foreign_key="step.id")
    content: str

    step: Step = Relationship(back_populates="theories")


class CodingTask(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    step_id: int = Field(foreign_key="step.id")
    instructions: str
    starter_code: str
    solution_code: str
    simple_test_expected_output: str
    advanced_test_code: str
    test_type: TestType
    points: int

    step: Step = Relationship(back_populates="coding_tasks")


class Test(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    step_id: int = Field(foreign_key="step.id")
    question: str
    points: int

    step: Step = Relationship(back_populates="tests")
    test_choices: list["TestChoice"] = Relationship(back_populates="test")


class TestChoice(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    test_id: int = Field(foreign_key="test.id")
    choice_text: str
    is_correct: bool

    test: Test = Relationship(back_populates="test_choices")
