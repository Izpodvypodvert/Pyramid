from backend.app.courses.models import Course
from backend.app.utils.repository import SQLModelRepository


class CoursesRepository(SQLModelRepository):
    model = Course
