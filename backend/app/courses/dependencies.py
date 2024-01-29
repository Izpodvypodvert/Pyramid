from typing import Annotated
from fastapi import Depends
from app.courses.models import Course
from app.courses.service import CoursesService
from app.utils.transaction_manager import TManagerDep


def get_courses_service(
    transaction_manager: TManagerDep,
) -> CoursesService:
    return CoursesService(Course, transaction_manager)


CoursesServiceDep = Annotated[CoursesService, Depends(get_courses_service)]
