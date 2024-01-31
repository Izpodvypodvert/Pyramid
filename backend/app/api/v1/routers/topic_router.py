from fastapi import APIRouter, Depends, HTTPException, status

from app.courses.models import Topic
from app.utils.exceptions import OpenAPIDocExtraResponse

from app.users.models import User
from app.users.dependencies import current_user
from app.courses.dependencies import TopicsServiceDep
from app.courses.schemas import TopicCreate, TopicUpdate


router = APIRouter(prefix="/topics", tags=["topics"])


@router.get(
    "/",
    response_model=list[Topic],
)
async def get_topics(topics_service: TopicsServiceDep):
    """Returns all topics"""
    topics = await topics_service.get_all()
    return topics


@router.get(
    "/{topic_id}",
    response_model=Topic,
    responses={
        404: {"model": OpenAPIDocExtraResponse},
    },
)
async def get_topic(topic_id: int, topics_service: TopicsServiceDep):
    """Returns specific topic by id"""
    topic = await topics_service.get_by_id(topic_id)
    return topic


@router.post(
    "/",
    response_model=Topic,
    responses={
        401: {"model": OpenAPIDocExtraResponse},
        404: {"model": OpenAPIDocExtraResponse},
    },
)
async def create_topic(
    topic: TopicCreate,
    topics_service: TopicsServiceDep,
    user: User = Depends(current_user),
):
    """Creates  topic"""
    new_topic = await topics_service.create(topic)
    return new_topic


@router.put(
    "/{topic_id}",
    responses={
        401: {"model": OpenAPIDocExtraResponse},
        404: {"model": OpenAPIDocExtraResponse},
    },
)
async def update_topic(
    topic_id: int,
    topic: TopicUpdate,
    topics_service: TopicsServiceDep,
    user: User = Depends(current_user),
):
    """Updates topic"""
    await topics_service.update(
        topic_id=topic_id, topic=topic, user_id=user.id, is_admin=user.is_superuser
    )
    return {"message": f"Topic has been successfully updated"}


@router.delete(
    "/{topic_id}",
    responses={
        401: {"model": OpenAPIDocExtraResponse},
        404: {"model": OpenAPIDocExtraResponse},
    },
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_topic(
    topic_id: int, topics_service: TopicsServiceDep, user: User = Depends(current_user)
):
    """Deletes specific course of the author by id"""
    deleted_count = await topics_service.delete(
        topic_id=topic_id, user_id=user.id, is_admin=user.is_superuser
    )
    if deleted_count == 0:
        raise HTTPException(
            status_code=404, detail="Topic not found or unauthorized access"
        )
