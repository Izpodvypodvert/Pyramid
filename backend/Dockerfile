FROM python:3.12.1-slim

# Установите poetry
RUN pip install --no-cache-dir --upgrade pip poetry

RUN poetry config virtualenvs.create false

WORKDIR /app

COPY /backend/pyproject.toml /backend/poetry.lock* /app/

RUN poetry install --no-dev --no-interaction --no-ansi

COPY . /app/

#CMD ["tail", "-f", "/dev/null"]