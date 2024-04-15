from app.steps.models import CodingTask

from app.steps.dependencies import CodingTasksServiceDep
from app.steps.schemas import CodingTaskCreate, CodingTaskUpdate
from app.api.v1.routers.base_router import ParentItemRouterWithUser


coding_task_router = ParentItemRouterWithUser(
    model=CodingTask,
    model_create=CodingTaskCreate,
    model_update=CodingTaskUpdate,
    service=CodingTasksServiceDep,
    prefix="/coding-tasks",
    tags=["coding tasks"],
).router
