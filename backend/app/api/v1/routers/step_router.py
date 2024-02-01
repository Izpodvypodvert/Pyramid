from app.courses.models import Step
from app.users.dependencies import current_user
from app.courses.dependencies import StepsServiceDep
from app.courses.schemas import StepCreate, StepUpdate
from app.utils.router import BaseRouter


step_router = BaseRouter(
    model=Step,
    model_create=StepCreate,
    model_update=StepUpdate,
    service=StepsServiceDep,
    prefix="/steps",
    tags=["steps"],
).router
