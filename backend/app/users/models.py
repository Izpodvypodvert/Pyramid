import uuid
from datetime import datetime
from typing import TYPE_CHECKING
from pydantic import UUID4, EmailStr

from sqlmodel import SQLModel, Field, Relationship, AutoString

from app.courses.models import Course, Topic, Lesson
from app.submissions.models import Submission


class User(SQLModel, table=True):
    __tablename__ = "user"

    id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    username: str
    is_author: bool = False
    created_at: datetime = Field(default_factory=datetime.now)

    if TYPE_CHECKING:  # pragma: no cover
        email: str
    else:
        email: EmailStr = Field(
            sa_type=AutoString,
            sa_column_kwargs={"unique": True, "index": True},
            nullable=False,
        )
    hashed_password: str

    is_active: bool = Field(True, nullable=False)
    is_superuser: bool = Field(False, nullable=False)
    is_verified: bool = Field(False, nullable=False)

    courses: list["Course"] = Relationship(back_populates="author")
    topics: list["Topic"] = Relationship(back_populates="author")
    lessons: list["Lesson"] = Relationship(back_populates="author")
    submissions: list["Submission"] = Relationship(back_populates="student")
    student_courses: list["StudentCourse"] = Relationship(back_populates="student")
    favorites: list["Favorite"] = Relationship(back_populates="student")

    class Config:
        orm_mode = True


class StudentCourse(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    student_id: UUID4 = Field(foreign_key="user.id")
    course_id: int = Field(foreign_key="course.id")
    points_accumulated: int
    is_completed: bool
    completed_at: datetime

    student: User = Relationship(back_populates="student_courses")
    course: "Course" = Relationship(back_populates="student_courses")


class Favorite(SQLModel, table=True):
    id: int | None = Field(default=True, primary_key=True)
    student_id: UUID4 = Field(foreign_key="user.id")
    course_id: int = Field(foreign_key="course.id")
    created_at: datetime

    student: User = Relationship(back_populates="favorites")
    course: "Course" = Relationship(back_populates="favorites")
