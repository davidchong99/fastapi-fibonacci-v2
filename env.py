from pydantic_settings import BaseSettings


# These variables will be overridden if they exist in OS env
class Settings(BaseSettings):
    # Server configuration
    server_port: int = 8080
    server_log_level: str = "info"

    # Database configuration
    db_url: str = ""


SETTINGS = Settings()
