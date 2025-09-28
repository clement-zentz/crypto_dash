# backend/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME : str = "Crypto Dashboard API"
    # switch to --> postgresql://user:pass@host/db
    DATABASE_URL : str = "sqlite:///./crypto.db"

    class Config:
        env_file = ".env"

settings = Settings()