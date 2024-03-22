from celery import Celery
from celery.utils.log import get_task_logger

# broker=f"amqp://{s.rabbitmq_default_user}:{s.rabbitmq_default_pass}@localhost:5672//",

celery_app = Celery(
    "app.tasks",
    broker=f"amqp://rabbitmq:rabbitmq@localhost:5672//",
    backend="redis://localhost:6379",
)

celery_app.autodiscover_tasks(["app.tasks"])
# celery_app = Celery(
#     "tasks",
#     broker=f"amqp://rabbitmq:rabbitmq@rabbitmq:5672//",
#     backend="redis://redis:6379/0",
# )



# celery_app.autodiscover_tasks(["tasks"])

celery_app.conf.broker_connection_retry_on_startup = True
celery_app.conf.backend_connection_retry_on_startup = True

celery_logger = get_task_logger(__name__)
