from app.courses.models import Topic
from app.users.dependencies import current_user
from app.courses.dependencies import TopicsServiceDep
from app.courses.schemas import TopicCreate, TopicUpdate
from app.api.v1.routers.base_router import BaseRouterWithUser


topic_router = BaseRouterWithUser(
    model=Topic,
    model_create=TopicCreate,
    model_update=TopicUpdate,
    service=TopicsServiceDep,
    prefix="/topics",
    tags=["topics"],
).router
