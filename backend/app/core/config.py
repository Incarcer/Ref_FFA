from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # API settings
    API_V1_STR: str = "/api/v1"

    # Database settings
    DATABASE_URL: str

    # Security settings
    SECRET_KEY: str
    
    # Yahoo OAuth2 settings
    YAHOO_CLIENT_ID: str
    YAHOO_CLIENT_SECRET: str
    
    # Pydantic settings configuration
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

# Create a single instance of the settings to be used throughout the application
settings = Settings()
