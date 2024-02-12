from app.steps.models import CodingTask

from app.steps.dependencies import CodingTasksServiceDep
from app.steps.schemas import CodingTaskCreate, CodingTaskUpdate
from app.utils.router import BaseRouter


coding_task_router = BaseRouter(
    model=CodingTask,
    model_create=CodingTaskCreate,
    model_update=CodingTaskUpdate,
    service=CodingTasksServiceDep,
    prefix="/coding-tasks",
    tags=["coding tasks"],
).router
