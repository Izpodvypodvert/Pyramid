from app.courses.models import Course
from app.courses.dependencies import CoursesServiceDep
from app.courses.schemas import CourseCreate, CourseUpdate
from app.api.v1.routers.base_router import BaseRouterWithUser


course_router = BaseRouterWithUser(
    model=Course,
    model_create=CourseCreate,
    model_update=CourseUpdate,
    service=CoursesServiceDep,
    prefix="/courses",
    tags=["courses"],
).router
