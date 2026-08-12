import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Enterprise IAM & Auth Service PoC"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super-secret-enterprise-key-for-jwt")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///./iam.db"

settings = Settings()
