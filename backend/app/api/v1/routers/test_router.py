from app.steps.models import Test

from app.steps.dependencies import TestsServiceDep
from app.steps.schemas import TestCreate, TestUpdate
from app.api.v1.routers.base_router import ParentItemRouterWithUser


test_router = ParentItemRouterWithUser(
    model=Test,
    model_create=TestCreate,
    model_update=TestUpdate,
    service=TestsServiceDep,
    prefix="/tests",
    tags=["tests"],
).router
