from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_url: str = "mongodb+srv://peharjohan:nuZ55IGothfexZrF@cluster0.wkawne9.mongodb.net/?appName=Cluster0"
    jwt_secret: str = "supersecretkey"
    service_port: int = 8080

    class Config:
        env_file = ".env"

settings = Settings()