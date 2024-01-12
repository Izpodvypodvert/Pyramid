import uuid
from datetime import datetime
from typing import TYPE_CHECKING
from pydantic import UUID4, EmailStr

from fastapi_users_db_sqlmodel import SQLModelBaseUserDB
from sqlmodel import SQLModel, Field, Relationship, AutoString


if TYPE_CHECKING:
    from app.courses.models import Course
    from app.users.models import User
    from app.submissions.models import Submission


class User(SQLModel, table=True):
    __tablename__ = "user"

    id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    username: str
    is_author: bool
    created_at: datetime

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

    class Config:
        orm_mode = True

    courses: list["Course"] = Relationship(back_populates="author")
    submissions: list["Submission"] = Relationship(back_populates="student")
    student_courses: list["StudentCourse"] = Relationship(back_populates="student")
    favorites: list["Favorite"] = Relationship(back_populates="student")


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
