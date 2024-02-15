from app.submissions.models import Submission
from app.submissions.schemas import SubmissionCreate
from app.utils.router import BaseRouter
from app.submissions.dependencies import SubmissionsServiceDep


submission_router = BaseRouter(
    model=Submission,
    model_create=SubmissionCreate,
    model_update=Submission,
    service=SubmissionsServiceDep,
    prefix="/submission",
    tags=["submission"],
).router
