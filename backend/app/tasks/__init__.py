from .submission_tasks import hello_world
# cd backend/ && poetry run celery -A app.tasks.celery_app worker -l info
# cd backend/ && poetry run uvicorn  app.main:app --reload
# cd backend/ && poetry run celery -A app.tasks.celery_app inspect stats
# poetry.exe run celery --broker=amqp://rabbitmq:rabbitmq@localhost:5672// flower
