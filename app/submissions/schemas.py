from pydantic import BaseModel


class SubmissionCreate(BaseModel):
    step_id: int = 1
    submitted_answer: str = "print('string')"
