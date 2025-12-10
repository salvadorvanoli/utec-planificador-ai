"""Application configuration settings."""
import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # API Configuration
    app_name: str = "UTEC Planificador AI Agent"
    app_version: str = "2.0.0"
    debug: bool = Field(default=False, validation_alias="DEBUG")

    # OpenAI Configuration
    openai_api_key: str = Field(validation_alias="OPENAI_KEY")
    openai_model: str = Field(default="gpt-4o-mini", validation_alias="OPENAI_MODEL")
    openai_temperature: float = Field(default=0.7, validation_alias="OPENAI_TEMPERATURE")
    openai_max_tokens: int = Field(default=800, validation_alias="OPENAI_MAX_TOKENS")

    # Database Configuration
    database_url: str = Field(
        default="sqlite:///./utec_planificador.db",
        validation_alias="DATABASE_URL"
    )

    # Session Configuration
    session_max_messages: int = Field(default=50, validation_alias="SESSION_MAX_MESSAGES")

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "allow"


# Global settings instance
settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get or create settings instance."""
    global settings
    if settings is None:
        settings = Settings()
    return settings

