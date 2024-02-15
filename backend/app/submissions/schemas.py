from pydantic import BaseModel


class SubmissionCreate(BaseModel):
    step_id: int
    submitted_answer: str
