from app.courses.models import Course
from app.courses.dependencies import CoursesServiceDep
from app.courses.schemas import CourseCreate, CourseUpdate
from app.utils.router import BaseRouter


course_router = BaseRouter(
    model=Course,
    model_create=CourseCreate,
    model_update=CourseUpdate,
    service=CoursesServiceDep,
    prefix="/courses",
    tags=["courses"],
).router
