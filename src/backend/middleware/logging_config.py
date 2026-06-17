# Structured logging configuration for the TravelAgent application.
# Purpose: Provides timestamped, leveled log output to stdout for monitoring and debugging.
# All application logs go through the "travelagent" logger with a consistent format:
#   2026-06-17 14:30:00 | INFO     | travelagent | Fetching weather for: Paris
# Third-party loggers (uvicorn, httpx) are quietened to reduce noise.

import logging
import sys


def setup_logging(level: str = "INFO") -> None:
    """Initialize the application logger. Called once at startup in main.py."""
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Output to stdout so container orchestrators (Docker, K8s) can capture logs
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    app_logger = logging.getLogger("travelagent")
    app_logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    app_logger.addHandler(handler)
    # Prevent duplicate log entries by stopping propagation to root logger
    app_logger.propagate = False

    # Reduce noise from third-party libraries
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
