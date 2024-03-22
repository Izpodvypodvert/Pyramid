import bleach
from fastapi import HTTPException
from markdown import markdown
from pydantic import BaseModel, validator

from app.steps.models import TestType


class TheoryCreate(BaseModel):
    step_id: int
    content: str

    @validator("content")
    def validate_and_sanitize_markdown(cls, value):
        try:
            # Converting Markdown to HTML
            html = markdown(value)
            # Sanitizing HTML with bleach
            clean_html = bleach.clean(html)

            if not clean_html.strip():
                raise ValueError(
                    "Markdown content is not valid or empty after sanitization"
                )
        except Exception as e:
            raise HTTPException(
                status_code=422, detail=f"Invalid markdown content: {e}"
            )
        return value


class TheoryUpdate(TheoryCreate):
    step_id: int | None = None
    content: str | None = None


class CodingTaskCreate(BaseModel):
    step_id: int
    instructions: str
    starter_code: str
    solution_code: str
    simple_test_expected_output: str
    advanced_test_code: str
    test_type: TestType
    points: int


class CodingTaskUpdate(BaseModel):
    step_id: int | None = None
    instructions: str | None = None
    starter_code: str | None = None
    solution_code: str | None = None
    simple_test_expected_output: str | None = None
    advanced_test_code: str | None = None
    test_type: TestType | None = None
    points: int | None = None


class TestCreate(BaseModel):
    step_id: int
    question: str
    points: int


class TestUpdate(BaseModel):
    step_id: int | None = None
    question: str | None = None
    points: int | None = None


class TestChoiceCreate(BaseModel):
    test_id: int
    choice_text: str
    is_correct: bool


class TestChoiceUpdate(BaseModel):
    test_id: int | None = None
    choice_text: str | None = None
    is_correct: bool | None = None
