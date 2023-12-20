from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum


class StepKind(Enum):
    THEORY = "Theory"
    CODING_TASK = "CodingTask"
    TEST = "Test"


class TestType(Enum):
    SIMPLE = "Simple"
    ADVANCED = "Advanced"


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


class Course(SQLModel, table=True):
    course_id: int | None = Field(default=None, primary_key=True)
    author_id: int = Field(foreign_key="user.user_id")
    title: str
    programming_language: str
    description: str
    is_published: bool
    created_at: datetime

    author: User = Relationship(back_populates="courses")
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


class Step(SQLModel, table=True):
    step_id: int | None = Field(default=None, primary_key=True)
    lesson_id: int = Field(foreign_key="lesson.lesson_id")
    order: int
    step_kind: StepKind

    lesson: Lesson = Relationship(back_populates="steps")
    theories: list["Theory"] = Relationship(back_populates="step")
    coding_tasks: list["CodingTask"] = Relationship(back_populates="step")
    tests: list["Test"] = Relationship(back_populates="step")
    submissions: list["Submission"] = Relationship(back_populates="step")


class Theory(SQLModel, table=True):
    theory_id: int | None = Field(default=None, primary_key=True)
    step_id: int = Field(foreign_key="step.step_id")
    content: str

    step: Step = Relationship(back_populates="theories")


class CodingTask(SQLModel, table=True):
    coding_task_id: int | None = Field(default=None, primary_key=True)
    step_id: int = Field(foreign_key="step.step_id")
    instructions: str
    starter_code: str
    solution_code: str
    simple_test_expected_output: str
    advanced_test_code: str
    test_type: TestType
    points: int

    step: Step = Relationship(back_populates="coding_tasks")


class Test(SQLModel, table=True):
    test_id: int | None = Field(default=None, primary_key=True)
    step_id: int = Field(foreign_key="step.step_id")
    question: str
    points: int

    step: Step = Relationship(back_populates="tests")
    test_choices: list["TestChoice"] = Relationship(back_populates="test")


class TestChoice(SQLModel, table=True):
    test_choice_id: int | None = Field(default=None, primary_key=True)
    test_id: int = Field(foreign_key="test.test_id")
    choice_text: str
    is_correct: bool

    test: Test = Relationship(back_populates="test_choices")


class Submission(SQLModel, table=True):
    submission_id: int | None = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="user.user_id")
    step_id: int = Field(foreign_key="step.step_id")
    submitted_answer: str
    is_correct: bool
    points_awarded: int
    submitted_at: datetime

    step: Step = Relationship(back_populates="submissions")
    student: User = Relationship(back_populates="submissions")


class StudentCourse(SQLModel, table=True):
    student_course_id: int | None = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="user.user_id")
    course_id: int = Field(foreign_key="course.course_id")
    points_accumulated: int
    is_completed: bool
    completed_at: datetime

    student: User = Relationship(back_populates="student_courses")
    course: Course = Relationship(back_populates="student_courses")


class Favorite(SQLModel, table=True):
    favorite_id: int | None = Field(default=True, primary_key=True)
    student_id: int = Field(foreign_key="user.user_id")
    course_id: int = Field(foreign_key="course.course_id")
    created_at: datetime

    student: User = Relationship(back_populates="favorites")
    course: Course = Relationship(back_populates="favorites")


class PointsSystem(SQLModel, table=True):
    points_id: int | None = Field(default=None, primary_key=True)
    description: str
    points_value: int
