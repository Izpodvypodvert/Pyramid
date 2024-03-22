from app.steps.models import Test

from app.steps.dependencies import TestsServiceDep
from app.steps.schemas import TestCreate, TestUpdate
from app.utils.router import BaseRouter


test_router = BaseRouter(
    model=Test,
    model_create=TestCreate,
    model_update=TestUpdate,
    service=TestsServiceDep,
    prefix="/tests",
    tags=["tests"],
).router
