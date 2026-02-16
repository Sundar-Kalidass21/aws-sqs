from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # App
    APP_NAME: str = "AI Doc Processor"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@db:5432/docproc"
    
    # AWS / LocalStack
    AWS_REGION: str = "us-east-1"
    AWS_ACCESS_KEY_ID: str = "test"
    AWS_SECRET_ACCESS_KEY: str = "test"
    AWS_ENDPOINT_URL: Optional[str] = "http://localstack:4566" # Defaulting for docker
    SQS_QUEUE_URL: str = "http://localstack:4566/000000000000/doc-queue"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
