from fastapi import APIRouter, Depends, HTTPException, status

from app.courses.models import Topic
from app.utils.exceptions import OpenAPIDocExtraResponse

from app.users.models import User
from app.users.dependencies import current_user
from app.courses.dependencies import CoursesServiceDep
from app.courses.schemas import TopicCreate, TopicUpdate


router = APIRouter(prefix="/topics", tags=["topics"])


@router.get(
    "/",
    response_model=Topic,
)
async def get_topics(topic_service:)