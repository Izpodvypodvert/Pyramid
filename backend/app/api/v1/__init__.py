from app.api.v1.routers.user_router import router as user_router
from app.api.v1.routers.course_router import course_router
from app.api.v1.routers.topic_router import topic_router
from app.api.v1.routers.lesson_router import lesson_router
from app.api.v1.routers.step_router import step_router
from app.api.v1.routers.testchoice_router import test_choice_router
from app.api.v1.routers.test_router import test_router
from app.api.v1.routers.theory_router import theory_router
from app.api.v1.routers.codingtask_router import coding_task_router
from app.api.v1.routers.submission_router import submission_router
from app.api.v1.routers.progress import user_progress_router


routers_v1 = [
    user_router,
    course_router,
    topic_router,
    lesson_router,
    step_router,
    test_choice_router,
    test_router,
    theory_router,
    coding_task_router,
    submission_router,
    user_progress_router
]