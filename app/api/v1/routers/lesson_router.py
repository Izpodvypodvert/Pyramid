from app.courses.dependencies import LessonsServiceDep
from app.courses.models import Lesson
from app.courses.schemas import LessonCreate, LessonUpdate
from app.core.router import ParentItemRouterWithUser


lesson_router = ParentItemRouterWithUser(
    model=Lesson,
    model_create=LessonCreate,
    model_update=LessonUpdate,
    service=LessonsServiceDep,
    prefix="/lessons",
    tags=["lessons"],
).router
