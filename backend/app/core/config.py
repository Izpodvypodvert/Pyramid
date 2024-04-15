from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    postgres_user: str = ""
    postgres_password: str = ""
    postgres_db: str = ""
    host: str = ""
    localhost: str = ""
    database_url: str = ""
    test: bool = False

    test_postgres_user: str = ""
    test_postgres_password: str = ""
    postgres_test_db: str = ""
    test_database_url: str = ""

    secret: str = ""

    rabbitmq_default_user: str
    rabbitmq_default_pass: str

    class Config:
        env_file = ".env"


settings = Settings()
