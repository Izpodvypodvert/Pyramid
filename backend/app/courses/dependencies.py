from typing import Annotated
from fastapi import Depends
from app.courses.models import Course, Lesson, Topic
from app.courses.service import CoursesService, LessonsService, TopicsService
from app.utils.transaction_manager import TManagerDep


def get_courses_service(
    transaction_manager: TManagerDep,
) -> CoursesService:
    return CoursesService(Course, transaction_manager)


CoursesServiceDep = Annotated[CoursesService, Depends(get_courses_service)]


def get_topics_service(transaction_manager: TManagerDep) -> TopicsService:
    return TopicsService(Topic, transaction_manager)


TopicsServiceDep = Annotated[TopicsService, Depends(get_topics_service)]


def get_lessons_service(transaction_manager: TManagerDep) -> LessonsService:
    return LessonsService(Lesson, transaction_manager)


LessonsServiceDep = Annotated[LessonsService, Depends(get_lessons_service)]
