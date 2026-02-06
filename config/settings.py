from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Environment
    environment: str = "local"
    
    # API Keys
    gemini_api_key: str
    weather_api_key: Optional[str] = None
    news_api_key: Optional[str] = None
    
    # Feature Flags
    use_mock_data: bool = False  # Changed to False - use real APIs when available
    enable_translation: bool = True
    enable_weather: bool = True
    enable_news: bool = True
    
    # Logging
    log_level: str = "INFO"
    
    # Demo Settings
    demo_flight_number: str = "VY71299"
    demo_user_id: str = "P001"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Cached settings instance"""
    return Settings()
