from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship


if TYPE_CHECKING:
    from app.courses.models import Course
    from app.users.models import User
    from app.submissions.models import Submission


class User(SQLModel, table=True):
    user_id: int | None = Field(default=None, primary_key=True)
    username: str
    email: str
    password_hash: str
    is_author: bool
    created_at: datetime

    courses: list["Course"] = Relationship(back_populates="author")
    submissions: list["Submission"] = Relationship(back_populates="student")
    student_courses: list["StudentCourse"] = Relationship(back_populates="student")
    favorites: list["Favorite"] = Relationship(back_populates="student")


class StudentCourse(SQLModel, table=True):
    student_course_id: int | None = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="user.user_id")
    course_id: int = Field(foreign_key="course.course_id")
    points_accumulated: int
    is_completed: bool
    completed_at: datetime

    student: User = Relationship(back_populates="student_courses")
    course: "Course" = Relationship(back_populates="student_courses")


class Favorite(SQLModel, table=True):
    favorite_id: int | None = Field(default=True, primary_key=True)
    student_id: int = Field(foreign_key="user.user_id")
    course_id: int = Field(foreign_key="course.course_id")
    created_at: datetime

    student: User = Relationship(back_populates="favorites")
    course: "Course" = Relationship(back_populates="favorites")
