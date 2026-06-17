# Backend configuration loaded from environment variables (.env file).
# Centralizes settings for the API host, port, CORS policy, and security flags.

import logging

from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("travelagent")


class Settings(BaseSettings):
    API_HOST: str = "localhost"
    API_PORT: int = 8000

    # CORS_ORIGINS: Comma-separated list of allowed frontend origins.
    # Only these domains can make cross-origin requests to the API.
    # Change this in .env for production (e.g., "https://yourdomain.com").
    CORS_ORIGINS: str = "http://localhost:8501,http://localhost:3000"

    # KEYS_ROTATED: Security flag — set to True in .env after rotating all API keys.
    # If False, the app logs a warning at startup reminding you to rotate keys
    # that were previously exposed in git history.
    KEYS_ROTATED: bool = False

    @property
    def cors_origin_list(self) -> list[str]:
        """Parse comma-separated CORS_ORIGINS string into a list for FastAPI middleware."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    def warn_if_keys_not_rotated(self):
        """Log a startup warning if API keys haven't been rotated after git exposure."""
        if not self.KEYS_ROTATED:
            logger.warning(
                "API keys were previously committed to git history. "
                "Rotate all keys and set KEYS_ROTATED=true in .env."
            )

    class Config:
        env_file = ".env"
        extra = "allow"