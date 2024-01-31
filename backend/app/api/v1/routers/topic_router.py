from app.courses.models import Topic
from app.users.dependencies import current_user
from app.courses.dependencies import TopicsServiceDep
from app.courses.schemas import TopicCreate, TopicUpdate
from app.utils.router import BaseRouter


topic_router = BaseRouter(
    model=Topic,
    model_create=TopicCreate,
    model_update=TopicUpdate,
    service=TopicsServiceDep,
    prefix="/topics",
    tags=["topics"],
).router
