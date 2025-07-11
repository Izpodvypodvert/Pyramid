# Pyramid Project

## Описание

Pyramid — это современная образовательная платформа для изучения и обучения программированию. Платформа предоставляет интерактивные курсы по широкому спектру языков программирования. Она позволяет авторам курсов создавать и распространять свои курсы, а учащиеся могут подписываться на интересующие их курсы, проходить уроки, выполнять задания и отслеживать свой прогресс.

## Ключевые особенности

- Множество языков программирования и технологий.
- Инструменты для авторов курсов для создания, управления и публикации содержимого.
- Интерактивные уроки с практическими заданиями и тестами для учащихся.
- Система баллов и прогресса, позволяющая пользователям отслеживать своё обучение.
- Интегрированная система тестирования кода с использованием Celery для асинхронной обработки заданий.

## Технологический стек

- **Backend**: **FastAPI** для создания RESTful API, **Celery** для обработки фоновых задач, **SQLModel** для взаимодействия с базой данных.

- **Frontend**: **React** (в разработке) — будет использован для создания интерактивного пользовательского интерфейса.
- **Database**: **PostgreSQL** для надёжного и масштабируемого хранения данных.
- **Message Broker**: **RabbitMQ** для управления очередями сообщений между веб-серверами и фоновыми задачами.
- **Cache and Result Backend**: **Redis** для кэширования и хранения результатов задач Celery.
- **Containerization**: **Docker** для изоляции и упаковки приложения в контейнеры, обеспечивающие согласованность среды.

## Быстрый старт

### Предварительные требования

- Docker и Docker Compose

### Запуск проекта

1. Склонируйте репозиторий:

   ```
   git clone git@github.com:Izpodvypodvert/Pyramid.git
   ```

## Зарегистрируйте своего поставщика OAuth

- Go to the [Google API Console](https://console.cloud.google.com/apis).
- Create a new project and configure OAuth credentials.
- Set up your **Redirect URI** to point to your FastAPI callback endpoint, e.g., `http://localhost:8000/auth/google/callback`.
- Copy your **Client ID** and **Client Secret**.

## Переменные окружения

2. Создайте `.env` файл с необходимыми переменными окружения.

```bash
# PostgreSQL configuration
POSTGRES_USER=myuser
POSTGRES_PASSWORD=mypassword
POSTGRES_DB=mydatabase
DATABASE_URL=postgresql+asyncpg://myuser:mypassword@localhost/mydatabase

# JWT Secret key for authentication
SECRET=your_jwt_secret_key
CLIENT_ID=Client ID from provider
CLIENT_SECRET=Client Secret from provider
FRONTEND_BASE_URL=The base URL of your frontend application
FRONTEND_LOGIN_REDIRECT_URL=Login URL of your frontend application
FRONTEND_OAUTH_REDIRECT_URL=Defines the URL where the frontend application will redirect users after successful authentication through an OAuth provider

# SMTP credentials
EMAIL_ADDRESS=Your smtp email address
EMAIL_PASSWORD=Your smtp email or app password
SMTP_ADDRESS=smtp.gmail.com
SMTP_PORT=587
```

## Запустите docker

3. Запустите проект с помощью Docker Compose:

- `docker compose up --build -d` – Build and start the containers.

## API Документация

4. После запуска контейнеров api будет доступно на

- [Swagger UI](http://127.0.0.1:8000/docs)
- [Redoc](http://127.0.0.1:8000/redoc)

## TODO

- Добавить rate limiter для некоторых эндпоинтов (slowapi?)
- Создать отдельные исключения для каждого типа ошибки (например, EntityNotFoundException)
- Добавить кэширование для некоторых эндпоинтов
- Необходимо реализовать поиск по курсам

Примечание: Этот README является лишь шаблоном и будет обновляться по мере развития проекта.
