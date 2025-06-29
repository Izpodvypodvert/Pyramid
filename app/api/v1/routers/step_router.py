from app.courses.models import Step
from app.courses.dependencies import StepsServiceDep
from app.courses.schemas import StepCreate, StepUpdate
from app.core.router import ParentItemRouterWithUser


step_router = ParentItemRouterWithUser(
    model=Step,
    model_create=StepCreate,
    model_update=StepUpdate,
    service=StepsServiceDep,
    prefix="/steps",
    tags=["steps"],
).router

