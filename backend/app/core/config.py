from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # Application Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # Database
    DATABASE_URL: str

    # Yahoo API Credentials
    YAHOO_CLIENT_ID: str
    YAHOO_CLIENT_SECRET: str
    YAHOO_REDIRECT_URI: str

    # Frontend URL (for CORS and redirects)
    FRONTEND_URL: str = "http://localhost:5173"
    
    API_V1_STR: str = "/api/v1"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()