from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Optional
from pydantic import UUID4
from sqlmodel import SQLModel, Field, Relationship

from app.steps.models import CodingTask, Test, Theory
from app.utils.mixins import HashMixin


if TYPE_CHECKING:
    from app.submissions.models import Submission
    from app.users.models import User, StudentCourse, Favorite, UserProgress


class BaseModel(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    author_id: UUID4 = Field(foreign_key="user.id")
    title: str
    description: str
    is_published: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Course(HashMixin, BaseModel, table=True):
    programming_language: str

    author: "User" = Relationship(back_populates="courses")
    student_courses: list["StudentCourse"] = Relationship(back_populates="course")
    favorites: list["Favorite"] = Relationship(back_populates="course")
    topics: list["Topic"] = Relationship(back_populates="course")
    steps: list["Step"] = Relationship(back_populates="course")
    user_progress: list["UserProgress"] = Relationship(back_populates="course")


class Topic(HashMixin, BaseModel, table=True):
    course_id: int = Field(foreign_key="course.id")
    order: int

    author: "User" = Relationship(back_populates="topics")
    course: Course = Relationship(back_populates="topics")
    lessons: list["Lesson"] = Relationship(back_populates="topic")


class Lesson(HashMixin, BaseModel, table=True):
    topic_id: int = Field(foreign_key="topic.id")
    order: int

    author: "User" = Relationship(back_populates="lessons")
    topic: Topic = Relationship(back_populates="lessons")
    steps: list["Step"] = Relationship(back_populates="lesson")
    user_progress: list["UserProgress"] = Relationship(back_populates="lesson")


class StepKind(Enum):
    THEORY = "Theory"
    CODING_TASK = "CodingTask"
    TEST = "Test"


class Step(HashMixin, SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    course_id: int = Field(foreign_key="course.id")
    lesson_id: int = Field(foreign_key="lesson.id")
    order: int
    step_kind: StepKind
    author_id: UUID4 = Field(foreign_key="user.id")
    is_published: bool = False

    course: "Course" = Relationship(back_populates="steps")
    lesson: "Lesson" = Relationship(back_populates="steps")
    theory: Optional["Theory"] = Relationship(
        back_populates="step", sa_relationship_kwargs={"lazy": "selectin"}
    )
    coding_task: Optional["CodingTask"] = Relationship(
        back_populates="step", sa_relationship_kwargs={"lazy": "selectin"}
    )
    test: Optional["Test"] = Relationship(
        back_populates="step", sa_relationship_kwargs={"lazy": "selectin"}
    )
    submissions: list["Submission"] = Relationship(back_populates="step")
    user_progress: list["UserProgress"] = Relationship(back_populates="step")
