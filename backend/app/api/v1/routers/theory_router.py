from app.steps.models import Theory

from app.steps.dependencies import TheoriesServiceDep
from app.steps.schemas import TheoryCreate, TheoryUpdate
from app.utils.router import BaseRouter


theory_router = BaseRouter(
    model=Theory,
    model_create=TheoryCreate,
    model_update=TheoryUpdate,
    service=TheoriesServiceDep,
    prefix="/theories",
    tags=["theories"],
).router
