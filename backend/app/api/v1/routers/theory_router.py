from app.steps.models import Theory

from app.steps.dependencies import TheoriesServiceDep
from app.steps.schemas import TheoryCreate, TheoryUpdate
from app.api.v1.routers.base_router import ParentItemRouterWithUser


theory_router = ParentItemRouterWithUser(
    model=Theory,
    model_create=TheoryCreate,
    model_update=TheoryUpdate,
    service=TheoriesServiceDep,
    prefix="/theories",
    tags=["theories"],
).router
