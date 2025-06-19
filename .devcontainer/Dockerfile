FROM python:3.12.1-slim

RUN pip install --no-cache-dir --upgrade pip poetry

RUN poetry config virtualenvs.create false

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

RUN poetry install --without dev --no-interaction --no-ansi

COPY . /app/

#CMD ["tail", "-f", "/dev/null"]