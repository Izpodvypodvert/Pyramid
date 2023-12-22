from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship


if TYPE_CHECKING:
    from app.users.models import User, StudentCourse, Favorite
    from app.steps.models import Step


class Course(SQLModel, table=True):
    course_id: int | None = Field(default=None, primary_key=True)
    author_id: int = Field(foreign_key="user.user_id")
    title: str
    programming_language: str
    description: str
    is_published: bool
    created_at: datetime

    author: "User" = Relationship(back_populates="courses")
    student_courses: list["StudentCourse"] = Relationship(back_populates="course")
    favorites: list["Favorite"] = Relationship(back_populates="course")


class Topic(SQLModel, table=True):
    topic_id: int | None = Field(default=None, primary_key=True)
    course_id: int = Field(foreign_key="course.course_id")
    title: str
    description: str
    order: int

    course: Course = Relationship(back_populates="topics")
    lessons: list["Lesson"] = Relationship(back_populates="topic")


class Lesson(SQLModel, table=True):
    lesson_id: int | None = Field(default=None, primary_key=True)
    topic_id: int = Field(foreign_key="topic.topic_id")
    title: str
    description: str
    order: int

    topic: Topic = Relationship(back_populates="lessons")
    steps: list["Step"] = Relationship(back_populates="lesson")
