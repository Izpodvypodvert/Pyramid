from app.steps.models import TestChoice

from app.steps.dependencies import TestChoicesServiceDep
from app.steps.schemas import TestChoiceCreate, TestChoiceUpdate
from app.utils.router import BaseRouter


test_choice_router = BaseRouter(
    model=TestChoice,
    model_create=TestChoiceCreate,
    model_update=TestChoiceUpdate,
    service=TestChoicesServiceDep,
    prefix="/test-choices",
    tags=["test choices"],
).router
