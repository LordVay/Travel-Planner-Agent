# Agent API key configuration with security validation.
# Loads external service API keys from .env and validates they are not placeholders.
# This prevents the app from starting with dummy keys that would silently fail at runtime.

from pydantic import field_validator
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class AgentSettings(BaseSettings):
    WEATHER_API: str   # OpenWeatherMap API key
    GEMINI_API: str    # Google Gemini LLM API key
    FLIGHT_API: str    # Flight data API key
    MAPS_API: str      # Google Maps API key

    @field_validator("*", mode="before")
    @classmethod
    def reject_placeholder_keys(cls, v):
        """Fail fast if any API key is a known placeholder value.
        This catches misconfigured .env files before they cause cryptic runtime errors."""
        placeholders = {"your-api-key", "change_me", "xxx", "placeholder", ""}
        if isinstance(v, str) and v.strip().lower() in placeholders:
            raise ValueError("API key appears to be a placeholder. Set a real key in .env.")
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"
