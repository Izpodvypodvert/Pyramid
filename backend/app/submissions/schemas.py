from pydantic import BaseModel

from app.courses.models import StepKind


class SubmissionCreate(BaseModel):
    step_id: int = 1
    submitted_answer: str = "print('privet')"
