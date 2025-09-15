from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Application Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # Yahoo API Credentials
    YAHOO_CLIENT_ID: str
    YAHOO_CLIENT_SECRET: str
    YAHOO_REDIRECT_URI: str

    # Frontend URL (for CORS and redirects)
    FRONTEND_URL: str = "http://localhost:5173"
    
    API_V1_STR: str = "/api/v1"

    # Database URL
    DATABASE_URL: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()