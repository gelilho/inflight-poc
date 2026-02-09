from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Environment
    environment: str = "local"

    # API Keys — only Gemini needed (single AI engine for all content)
    gemini_api_key: str

    # Feature Flags
    use_mock_data: bool = False
    enable_translation: bool = True

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
