from typing import Annotated
from fastapi import Depends

from app.core.transaction_manager import TManagerDep
from app.users.dependencies import UserManager, get_user_manager
from app.steps.service import (
    CodingTasksService,
    TestChoicesService,
    TestsService,
    TheoriesService,
)
from app.steps.models import CodingTask, Test, TestChoice, Theory


def get_theory_service(
    transaction_manager: TManagerDep,
    user_manager: UserManager = Depends(get_user_manager),
) -> TheoriesService:
    return TheoriesService(Theory, transaction_manager, user_manager)


TheoriesServiceDep = Annotated[TheoriesService, Depends(get_theory_service)]


def get_coding_task_service(
    transaction_manager: TManagerDep,
    user_manager: UserManager = Depends(get_user_manager),
) -> CodingTasksService:
    return CodingTasksService(CodingTask, transaction_manager, user_manager)


CodingTasksServiceDep = Annotated[CodingTasksService, Depends(get_coding_task_service)]


def get_test_service(
    transaction_manager: TManagerDep,
    user_manager: UserManager = Depends(get_user_manager),
) -> TestsService:
    return TestsService(Test, transaction_manager, user_manager)


TestsServiceDep = Annotated[TestsService, Depends(get_test_service)]


def get_test_choice_service(
    transaction_manager: TManagerDep,
    user_manager: UserManager = Depends(get_user_manager),
) -> TestChoicesService:
    return TestChoicesService(TestChoice, transaction_manager, user_manager)


TestChoicesServiceDep = Annotated[TestChoicesService, Depends(get_test_choice_service)]
