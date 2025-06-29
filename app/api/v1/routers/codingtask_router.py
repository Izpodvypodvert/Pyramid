from app.core.router import ParentItemRouterWithUser
from app.steps.dependencies import CodingTasksServiceDep
from app.steps.models import CodingTask
from app.steps.schemas import CodingTaskCreate, CodingTaskUpdate

coding_task_router = ParentItemRouterWithUser(
    model=CodingTask,
    model_create=CodingTaskCreate,
    model_update=CodingTaskUpdate,
    service=CodingTasksServiceDep,
    prefix="/coding-tasks",
    tags=["coding tasks"],
).router
