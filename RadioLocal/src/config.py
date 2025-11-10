from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_url: str
    jwt_secret: str
    service_port: int = 8080

    class Config:
        env_file = ".env"

settings = Settings()