from fastapi import APIRouter, Depends

from app.users.dependencies import current_user, UserProgressServiceDep
from app.users.models import User, UserProgress


user_progress_router = APIRouter(prefix="/progress", tags=["progress"])


@user_progress_router.get("/{lesson_id}", response_model=list[UserProgress])
async def get_user_steps_progress(
    lesson_id: int,
    service: UserProgressServiceDep,
    user: User = Depends(current_user),
):
    progress = await service.get_user_steps_progress(lesson_id, user)
    return progress


@user_progress_router.get("/", response_model=list[UserProgress])
async def get_user_lessons_progress(
    service: UserProgressServiceDep,
    user: User = Depends(current_user),
):
    progress = await service.get_user_lessons_progress(user)
    return progress
