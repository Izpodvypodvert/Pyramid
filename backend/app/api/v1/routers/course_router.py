from fastapi import APIRouter, Depends, HTTPException, status

from app.courses.models import Course
from app.utils.exceptions import OpenAPIDocExtraResponse

from app.users.models import User
from app.users.dependencies import current_user
from app.courses.dependencies import CoursesServiceDep
from app.courses.schemas import CourseCreate, CourseUpdate


router = APIRouter(prefix="/courses", tags=["courses"])


@router.get(
    "/",
    response_model=list[Course],
)
async def get_courses(
    course_service: CoursesServiceDep,
):
    """Returns all curses"""
    courses = await course_service.get_all()
    return courses


@router.get(
    "/{course_id}",
    response_model=Course,
    responses={
        404: {"model": OpenAPIDocExtraResponse},
    },
)
async def get_course(
    course_id: int,
    course_service: CoursesServiceDep,
):
    """Returns specific course by id"""
    course = await course_service.get_by_id(course_id)
    return course


@router.delete(
    "/{course_id}",
    responses={
        401: {"model": OpenAPIDocExtraResponse},
        404: {"model": OpenAPIDocExtraResponse},
    },
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_course(
    course_id: int,
    course_service: CoursesServiceDep,
    user: User = Depends(current_user),
):
    """Deletes specific course of the author by id"""
    deleted_count = await course_service.delete(
        course_id=course_id, user_id=user.id, is_admin=user.is_superuser
    )
    if deleted_count == 0:
        raise HTTPException(
            status_code=404, detail="Course not found or unauthorized access"
        )


@router.post(
    "/",
    response_model=Course,
    responses={
        401: {"model": OpenAPIDocExtraResponse},
        404: {"model": OpenAPIDocExtraResponse},
    },
)
async def create_course(
    course: CourseCreate,
    course_service: CoursesServiceDep,
    user: User = Depends(current_user),
):
    """Creates  course"""
    new_course = await course_service.create(course)
    return new_course


@router.put(
    "/{course_id}",
    responses={
        401: {"model": OpenAPIDocExtraResponse},
        404: {"model": OpenAPIDocExtraResponse},
    },
)
async def update_course(
    course_id: int,
    course: CourseUpdate,
    course_service: CoursesServiceDep,
    user: User = Depends(current_user),
):
    """Update course"""
    await course_service.update(
        course_id=course_id, course=course, user_id=user.id, is_admin=user.is_superuser
    )
    return {"message": f"Course has been successfully updated"}
