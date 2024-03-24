import os
from celery import Celery
from celery.utils.log import get_task_logger


rabbitmq_user = os.environ['RABBITMQ_DEFAULT_USER']
rabbitmq_pass = os.environ['RABBITMQ_DEFAULT_PASS']

celery_app = Celery(
    "app.tasks",
    broker=f"amqp://{rabbitmq_user}:{rabbitmq_pass}@rabbitmq:5672//",
    backend="redis://redis:6379",
)

celery_app.autodiscover_tasks(["app.tasks"])

celery_app.conf.broker_connection_retry_on_startup = True
celery_app.conf.backend_connection_retry_on_startup = True

celery_logger = get_task_logger(__name__)
