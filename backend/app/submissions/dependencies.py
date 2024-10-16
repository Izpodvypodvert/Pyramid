from typing import Annotated
from fastapi import Depends

from app.core.transaction_manager import TManagerDep
from app.submissions.models import Submission
from app.submissions.service import SubmissionsService
from app.users.dependencies import UserManager, get_user_manager



def get_submission_service(
    transaction_manager: TManagerDep,
    user_manager: UserManager = Depends(get_user_manager),
) -> SubmissionsService:
    return SubmissionsService(Submission, transaction_manager, user_manager)


SubmissionsServiceDep = Annotated[SubmissionsService, Depends(get_submission_service)]
