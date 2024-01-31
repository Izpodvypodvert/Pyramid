from fastapi import APIRouter, Depends, HTTPException, status
from typing import Type, Generic, TypeVar, List

from app.courses.models import Course, Topic
from app.courses.service import CoursesService, TopicsService

T = TypeVar("T")  # Тип модели данных
S = TypeVar("S")  # Тип сервиса


class CRUDRouter(Generic[T, S]):
    def __init__(self, model: Type[T], service: Type[S], prefix: str, tags: List[str]):
        self.router = APIRouter(prefix=prefix, tags=tags)
        self.model = model
        self.service = service
        self._create_routes()

    def _create_routes(self):
        @self.router.get("/", response_model=List[self.model])
        async def read_items(service: self.service = Depends()):
            return await service.get_all()

        @self.router.get("/{item_id}", response_model=self.model)
        async def read_item(item_id: int, service: self.service = Depends()):
            item = await service.get_by_id(item_id)
            if not item:
                raise HTTPException(status_code=404, detail="Item not found")
            return item

        # Здесь вы можете добавить другие маршруты (POST, PUT, DELETE и т.д.)


# Пример использования CRUDRouter для Courses
courses_router = CRUDRouter(
    model=Course, service=CoursesService, prefix="/courses", tags=["courses"]
).router

# Пример использования CRUDRouter для Topics
topics_router = CRUDRouter(
    model=Topic, service=TopicsService, prefix="/topics", tags=["topics"]
).router
