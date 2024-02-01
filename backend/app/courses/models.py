from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING
from pydantic import UUID4
from sqlmodel import SQLModel, Field, Relationship

from app.steps.models import CodingTask, Test, Theory


if TYPE_CHECKING:
    from app.submissions.models import Submission
    from app.users.models import User, StudentCourse, Favorite


class Course(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    author_id: UUID4 = Field(foreign_key="user.id")
    title: str
    programming_language: str
    description: str
    is_published: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

    author: "User" = Relationship(back_populates="courses")
    student_courses: list["StudentCourse"] = Relationship(back_populates="course")
    favorites: list["Favorite"] = Relationship(back_populates="course")
    topics: list["Topic"] = Relationship(back_populates="course")

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, Course):
            return self.id == other.id
        return False


class Topic(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    author_id: UUID4 = Field(foreign_key="user.id")
    course_id: int = Field(foreign_key="course.id")
    title: str
    description: str
    is_published: bool = False
    order: int

    author: "User" = Relationship(back_populates="topics")
    course: Course = Relationship(back_populates="topics")
    lessons: list["Lesson"] = Relationship(back_populates="topic")

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, Topic):
            return self.id == other.id
        return False


class Lesson(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    author_id: UUID4 = Field(foreign_key="user.id")
    topic_id: int = Field(foreign_key="topic.id")
    title: str
    description: str
    is_published: bool = False
    order: int

    author: "User" = Relationship(back_populates="lessons")
    topic: Topic = Relationship(back_populates="lessons")
    steps: list["Step"] = Relationship(back_populates="lesson")

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, Lesson):
            return self.id == other.id
        return False


class StepKind(Enum):
    THEORY = "Theory"
    CODING_TASK = "CodingTask"
    TEST = "Test"


class Step(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    lesson_id: int = Field(foreign_key="lesson.id")
    order: int
    step_kind: StepKind
    author_id: UUID4 = Field(foreign_key="user.id")
    is_published: bool = False

    lesson: "Lesson" = Relationship(back_populates="steps")
    theories: list["Theory"] = Relationship(back_populates="step")
    coding_tasks: list["CodingTask"] = Relationship(back_populates="step")
    tests: list["Test"] = Relationship(back_populates="step")
    submissions: list["Submission"] = Relationship(back_populates="step")

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, Step):
            return self.id == other.id
        return False
