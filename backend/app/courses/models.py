from datetime import datetime
from typing import TYPE_CHECKING
from pydantic import UUID4

from sqlmodel import SQLModel, Field, Relationship

from app.steps.models import Step

if TYPE_CHECKING:
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


class Topic(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    course_id: int = Field(foreign_key="course.id")
    title: str
    description: str
    order: int

    course: Course = Relationship(back_populates="topics")
    lessons: list["Lesson"] = Relationship(back_populates="topic")


class Lesson(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    topic_id: int = Field(foreign_key="topic.id")
    title: str
    description: str
    order: int

    topic: Topic = Relationship(back_populates="lessons")
    steps: list["Step"] = Relationship(back_populates="lesson")
