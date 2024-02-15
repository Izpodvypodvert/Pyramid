from app.submissions.models import Submission
from app.utils.repository import SQLModelRepository


class SubmissionRepository(SQLModelRepository):
    model = Submission
