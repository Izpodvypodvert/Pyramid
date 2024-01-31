from fastapi import HTTPException
from pydantic import UUID4, BaseModel, validator


class CourseCreate(BaseModel):
    author_id: UUID4
    title: str
    programming_language: str
    description: str


class CourseUpdate(BaseModel):
    author_id: UUID4
    title: str | None = None
    programming_language: str | None = None
    description: str | None = None
    is_published: bool | None = None


class BaseModelWithOrder(BaseModel):
    order: int

    @validator("order")
    def validate_order(cls, value):
        if value is not None and value < 0:
            raise HTTPException(status_code=400, detail="Order must be greater than 0")
        return value


class TopicCreate(BaseModelWithOrder):
    author_id: UUID4
    course_id: int
    title: str
    description: str


class TopicUpdate(TopicCreate):
    course_id: int | None = None
    title: str | None = None
    description: str | None = None
    order: int | None = None


class LessonCreate(BaseModelWithOrder):
    author_id: UUID4
    topic_id: int
    title: str
    description: str


class LessonUpdate(LessonCreate):
    topic_id: int | None = None
    title: str | None = None
    description: str | None = None
    order: int | None = None
