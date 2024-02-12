from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routers.user_router import router as user_router
from app.api.v1.routers.course_router import course_router
from app.api.v1.routers.topic_router import topic_router
from app.api.v1.routers.lesson_router import lesson_router
from app.api.v1.routers.step_router import step_router
from app.api.v1.routers.testchoice_router import test_choice_router
from app.api.v1.routers.test_router import test_router
from app.api.v1.routers.theory_router import theory_router
from app.api.v1.routers.codingtask_router import coding_task_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)

app.include_router(user_router)
app.include_router(course_router)
app.include_router(topic_router)
app.include_router(lesson_router)
app.include_router(step_router)
app.include_router(test_choice_router)
app.include_router(test_router)
app.include_router(theory_router)
app.include_router(coding_task_router)
