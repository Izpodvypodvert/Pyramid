# Используйте базовый образ Python
FROM python:3.12.1-slim

# Установите необходимые пакеты для добавления репозитория Docker
RUN apt-get update && \
    apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# Добавьте официальный GPG ключ Docker
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Добавьте репозиторий Docker в список источников APT
RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian \
    $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

# Установите Docker CLI
RUN apt-get update && \
    apt-get install -y docker-ce-cli

# Установка зависимостей
RUN pip install --upgrade pip
# COPY requirements.txt /tmp/
RUN pip install redis celery flower

# Копирование задач в контейнер
WORKDIR /app
COPY /backend/app/tasks /app/tasks

# Запуск Celery worker
#CMD celery -A tasks worker --loglevel=info