from typing import Annotated
from fastapi import Depends

from app.courses.models import Course, Lesson, Step, Topic
from app.courses.service import (
    CoursesService,
    LessonsService,
    StepsService,
    TopicsService,
)
from app.utils.transaction_manager import TManagerDep
from app.users.dependencies import UserManager, get_user_manager


def get_courses_service(
    transaction_manager: TManagerDep,
    user_manager: UserManager = Depends(get_user_manager),
) -> CoursesService:
    return CoursesService(Course, transaction_manager, user_manager)


CoursesServiceDep = Annotated[CoursesService, Depends(get_courses_service)]


def get_topics_service(
    transaction_manager: TManagerDep,
    user_manager: UserManager = Depends(get_user_manager),
) -> TopicsService:
    return TopicsService(Topic, transaction_manager, user_manager)


TopicsServiceDep = Annotated[TopicsService, Depends(get_topics_service)]


def get_lessons_service(
    transaction_manager: TManagerDep,
    user_manager: UserManager = Depends(get_user_manager),
) -> LessonsService:
    return LessonsService(Lesson, transaction_manager, user_manager)


LessonsServiceDep = Annotated[LessonsService, Depends(get_lessons_service)]


def get_steps_service(
    transaction_manager: TManagerDep,
    user_manager: UserManager = Depends(get_user_manager),
) -> StepsService:
    return StepsService(Step, transaction_manager, user_manager)


StepsServiceDep = Annotated[StepsService, Depends(get_steps_service)]
