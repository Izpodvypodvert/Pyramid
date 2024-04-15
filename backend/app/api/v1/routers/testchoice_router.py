from app.steps.models import TestChoice

from app.steps.dependencies import TestChoicesServiceDep
from app.steps.schemas import TestChoiceCreate, TestChoiceUpdate
from app.api.v1.routers.base_router import ParentItemRouterWithUser


test_choice_router = ParentItemRouterWithUser(
    model=TestChoice,
    model_create=TestChoiceCreate,
    model_update=TestChoiceUpdate,
    service=TestChoicesServiceDep,
    prefix="/test-choices",
    tags=["test choices"],
).router
