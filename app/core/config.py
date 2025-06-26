from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    project_name: str = ""
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

    email_address: str = ""
    email_password: str = ""
    smtp_address: str = ""
    smtp_port: int = 587

    class Config:
        env_file = ".devcontainer/.env"

    @property
    def reset_password_url(self):
        return f"{self.frontend_base_url}/reset-password?token"

    @property
    def verification_url(self):
        return f"{self.frontend_base_url}/verify-email?token"


settings = Settings()
