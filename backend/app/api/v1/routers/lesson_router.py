from app.courses.dependencies import LessonsServiceDep
from app.courses.models import Lesson
from app.courses.schemas import LessonCreate, LessonUpdate
from app.api.v1.routers.base_router import BaseRouterWithUser


lesson_router = BaseRouterWithUser(
    model=Lesson,
    model_create=LessonCreate,
    model_update=LessonUpdate,
    service=LessonsServiceDep,
    prefix="/lessons",
    tags=["lessons"],
).router
