from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    postgres_user: str = ""
    postgres_password: str = ""
    postgres_db: str = ""
    host: str = ""
    localhost: str = ""
    database_url: str = ""
    test: bool = True

    test_postgres_user: str = ""
    test_postgres_password: str = ""
    postgres_test_db: str = ""
    test_host: str = ""
    test_database_url: str = ""

    secret: str = ""

    rabbitmq_default_user: str = ""
    rabbitmq_default_pass: str = ""
    
    client_id: str = ""
    client_secret: str = ""
    frontend_base_url: str = ""
    frontend_login_redirect_url: str = ""
    frontend_oauth_redirect_url: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
