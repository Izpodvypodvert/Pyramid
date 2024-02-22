from fastapi import APIRouter, Depends
from app.submissions.dependencies import SubmissionsServiceDep
from app.submissions.models import Submission
from app.submissions.schemas import SubmissionCreate

from app.users.dependencies import current_user
from app.users.models import User
from app.utils.router import BaseRouter

from app.utils.exceptions import OpenAPIDocExtraResponse


# submission_router = BaseRouter(
#     model=Submission,
#     model_create=SubmissionCreate,
#     model_update=Submission,
#     service=SubmissionsServiceDep,
#     prefix="/submissions",
#     tags=["submissions"],
# ).router


submission_router = APIRouter(prefix="/submissions", tags=["submissions"])


@submission_router.post(
    "/",
    response_model=Submission,
    responses={
        401: {"model": OpenAPIDocExtraResponse},
        404: {"model": OpenAPIDocExtraResponse},
    },
)
async def create_submission(
    item: SubmissionCreate,
    service: SubmissionsServiceDep,
    user: User = Depends(current_user),
):
    new_submission = await service.create(item)
    return new_submission


@submission_router.get(
    "/{step_id}",
    response_model=list[Submission],
    responses={
        401: {"model": OpenAPIDocExtraResponse},
        404: {"model": OpenAPIDocExtraResponse},
    },
)
async def get_user_submissions_by_step_id(
    step_id: int,
    service: SubmissionsServiceDep,
    user: User = Depends(current_user),
):
    submissions = await service.get_user_submissions_by_step_id(step_id, user)
    return submissions
