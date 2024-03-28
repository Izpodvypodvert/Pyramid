from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship
from enum import Enum


if TYPE_CHECKING:
    from app.courses.models import Step


class TestType(Enum):
    SIMPLE = "Simple"
    ADVANCED = "Advanced"


class Theory(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    step_id: int = Field(foreign_key="step.id")
    content: str

    step: "Step" = Relationship(back_populates="theory")


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

    step: "Step" = Relationship(back_populates="coding_task")


class Test(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    step_id: int = Field(foreign_key="step.id")
    question: str
    points: int

    step: "Step" = Relationship(back_populates="test")
    test_choices: list["TestChoice"] = Relationship(back_populates="test")


class TestChoice(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    test_id: int = Field(foreign_key="test.id")
    choice_text: str
    is_correct: bool

    test: Test = Relationship(back_populates="test_choices")
