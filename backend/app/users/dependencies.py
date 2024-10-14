from typing import Annotated

from fastapi import Depends

from app.core.transaction_manager import TManagerDep
from app.users.models import  UserProgress
from app.users.service import UserProgressService
from app.users.manager import UserManager, get_user_manager


def get_user_progress_service(
    transaction_manager: TManagerDep,
    user_manager: UserManager = Depends(get_user_manager),
) -> UserProgressService:
    return UserProgressService(UserProgress, transaction_manager, user_manager)


UserProgressServiceDep = Annotated[
    UserProgressService, Depends(get_user_progress_service)
]
