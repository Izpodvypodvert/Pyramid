from app.courses.models import Topic
from app.users.auth_config import current_user
from app.courses.dependencies import TopicsServiceDep
from app.courses.schemas import TopicCreate, TopicUpdate
from app.core.router import ParentItemRouterWithUser


topic_router = ParentItemRouterWithUser(
    model=Topic,
    model_create=TopicCreate,
    model_update=TopicUpdate,
    service=TopicsServiceDep,
    prefix="/topics",
    tags=["topics"],
).router
