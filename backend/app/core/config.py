import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "SheetPilot AI Engine"
    API_V1_STR: str = "/api/v1"
    
    # Environment & Host
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # AI Engine Keys
    GEMINI_API_KEY: Optional[str] = None
    
    # Databases & Queues
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/sheetpilot"
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Local Storage Directory
    STORAGE_DIR: str = "storage"
    
    # Read environment variables from root .env or parent directory .env
    model_config = SettingsConfigDict(
        env_file=("../.env", ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()

# Ensure local storage directory exists
os.makedirs(settings.STORAGE_DIR, exist_ok=True)
