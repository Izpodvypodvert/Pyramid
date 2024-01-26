from fastapi import APIRouter, Depends

from app.courses.models import Course
from app.courses.service import CoursesService
from app.utils.exceptions import OpenAPIDocExtraResponse
from app.utils.transaction_manager import TManagerDep
from app.users.models import User
from app.users.dependencies import current_user


router = APIRouter(prefix="/courses", tags=["courses"])


@router.get(
    "", response_model=list[Course], responses={401: {"model": OpenAPIDocExtraResponse}}
)
async def get_courses(
    transaction_manager: TManagerDep,
):
    """Returns all curses"""
    courses = await CoursesService().get_courses(
        transaction_manager=transaction_manager
    )
    return courses


@router.get(
    "/{course_id}",
    response_model=Course,
    responses={
        401: {"model": OpenAPIDocExtraResponse},
        404: {"model": OpenAPIDocExtraResponse},
    },
)
async def get_course(
    course_id: int,
    transaction_manager: TManagerDep,
):
    """Returns specific course by id"""
    course = await CoursesService().get_course(
        transaction_manager=transaction_manager, course_id=course_id
    )
    return course


@router.delete(
    "{course_id}",
    response_model=Course,
    responses={
        401: {"model": OpenAPIDocExtraResponse},
        404: {"model": OpenAPIDocExtraResponse},
    },
)
async def delete_course(
    course_id: int, transaction_manager: TManagerDep, user: User = Depends(current_user)
):
    """Deletes specific course of the author by id"""
    deleted_course = CoursesService().delete_course(
        transaction_manager=transaction_manager, course_id=course_id, user_id=user.id
    )
    return deleted_course


@router.post(
    "/course_id",
    response_model=Course,
    responses={
        400: {"model": OpenAPIDocExtraResponse},
        401: {"model": OpenAPIDocExtraResponse},
        404: {"model": OpenAPIDocExtraResponse},
    },
)
async def create_course(
    transaction_manager: TManagerDep, user: User = Depends(current_user)
):
    """Creates  course"""
    new_course = CoursesService().create_course(
        transaction_manager=transaction_manager, user_id=user.id
    )
    return new_course