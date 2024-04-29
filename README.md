# Pyramid Project

## Описание

Pyramid — это современная образовательная платформа для изучения и обучения программированию. Платформа предоставляет интерактивные курсы по широкому спектру языков программирования. Она позволяет авторам курсов создавать и распространять свои курсы, а учащиеся могут подписываться на интересующие их курсы, проходить уроки, выполнять задания и отслеживать свой прогресс.

## Ключевые особенности

-   Множество языков программирования и технологий.
-   Инструменты для авторов курсов для создания, управления и публикации содержимого.
-   Интерактивные уроки с практическими заданиями и тестами для учащихся.
-   Система баллов и прогресса, позволяющая пользователям отслеживать своё обучение.
-   Интегрированная система тестирования кода с использованием Celery для асинхронной обработки заданий.

## Технологический стек

-   **Backend**: **FastAPI** для создания RESTful API, **Celery** для обработки фоновых задач, **SQLModel** для взаимодействия с базой данных.

-   **Frontend**: **React** (в разработке) — будет использован для создания интерактивного пользовательского интерфейса.
-   **Database**: **PostgreSQL** для надёжного и масштабируемого хранения данных.
-   **Message Broker**: **RabbitMQ** для управления очередями сообщений между веб-серверами и фоновыми задачами.
-   **Cache and Result Backend**: **Redis** для кэширования и хранения результатов задач Celery.
-   **Containerization**: **Docker** для изоляции и упаковки приложения в контейнеры, обеспечивающие согласованность среды.

## Быстрый старт

### Предварительные требования

-   Docker и Docker Compose

### Запуск проекта

1. Склонируйте репозиторий:
    ```
    git clone git@github.com:Izpodvypodvert/Pyramid.git
    ```

2. Создайте `.env` файл с необходимыми переменными окружения.

3. Запустите проект с помощью Docker Compose:
    ```
    docker-compose --env-file ./backend/.env up --build -d 
    ```

4. После запуска контейнеров api будет доступно на `http://localhost/docs`.

## TODO

-   Написать тесты для основных компонентов программы
-   Начать писать фронт

Примечание: Этот README является лишь шаблоном и будет обновляться по мере развития проекта.
