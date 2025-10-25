from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import Optional, Union


class Settings(BaseSettings):
    """Application settings"""

    # API Settings
    API_TITLE: str = "Nigerian Tax Reform AI Chatbot (2026)"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "AI-powered chatbot to help Nigerian taxpayers understand the 2026 tax reforms and calculate tax obligations"

    # Google Gemini API
    GOOGLE_API_KEY: str

    # Model Settings
    MODEL_NAME: str = "gemini-pro"
    TEMPERATURE: float = 0.7
    MAX_OUTPUT_TOKENS: int = 2048

    # CORS Settings
    CORS_ORIGINS: Union[str, list] = "*"

    @field_validator('CORS_ORIGINS', mode='before')
    @classmethod
    def parse_cors_origins(cls, v):
        """Parse CORS_ORIGINS from string or list"""
        if isinstance(v, str):
            # If it's a single asterisk, return as list
            if v == "*":
                return ["*"]
            # If it's a comma-separated string, split it
            return [origin.strip() for origin in v.split(",")]
        return v

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
