from fastapi import APIRouter, Depends
from app.submissions.dependencies import SubmissionsServiceDep
from app.submissions.models import Submission
from app.submissions.schemas import SubmissionCreate

from app.users.auth_config import current_user
from app.users.models import User

from app.utils.exceptions import OpenAPIDocExtraResponse


submission_router = APIRouter(prefix="/submissions", tags=["submissions"])


@submission_router.post(
    "/",
    response_model=None,
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
    updated_item = item.model_dump()
    updated_item.update({"student_id": user.id})
    result = await service.create(updated_item)

    return result


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
