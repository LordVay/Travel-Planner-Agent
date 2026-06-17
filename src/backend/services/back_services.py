# Service layer that bridges the FastAPI routes with the CrewAI agent system.
# Each function validates input, logs the request, and delegates to the appropriate crew.

import logging

from ...agents.crew import weather_crew
from ...agents.crew import attraction_crew
from ...agents.crew import hotel_crew
from ...agents.crew import restaurant_crew
from ...agents.crew import itenerary_crew

# Structured logger replaces print() to enable log levels, timestamps, and filtering
logger = logging.getLogger("travelagent")


def get_weather_forecast(location: str) -> dict:
    input_data = {"location": location}
    try:
        logger.info(f"Fetching weather forecast for: {location}")
        result = weather_crew.kickoff(input_data)
        return result.to_dict()
    except ValueError as e:
        logger.warning(f"Invalid location: {e}")
        raise


def get_attraction_guide(location: str) -> dict:
    input_data = {"location": location}
    try:
        logger.info(f"Fetching attractions for: {location}")
        result = attraction_crew.kickoff(input_data)
        return result.to_dict()
    except ValueError as e:
        logger.warning(f"Invalid location: {e}")
        raise


def get_itenerary(location: str, days: int) -> dict:
    input_data = {"location": location, "days": days}
    try:
        logger.info(f"Generating {days}-day itinerary for: {location}")
        result = itenerary_crew.kickoff(input_data)
        return result.to_dict()
    except ValueError as e:
        logger.warning(f"Invalid location or days: {e}")
        raise


def get_hotel_recommendation(location: str) -> dict:
    input_data = {"location": location}
    try:
        logger.info(f"Finding hotels in: {location}")
        result = hotel_crew.kickoff(input_data)
        return result.to_dict()
    except ValueError as e:
        logger.warning(f"Invalid location: {e}")
        raise


def get_restaurant_recommendation(location: str) -> dict:
    input_data = {"location": location}
    try:
        logger.info(f"Finding restaurants in: {location}")
        result = restaurant_crew.kickoff(input_data)
        return result.to_dict()
    except ValueError as e:
        logger.warning(f"Invalid location: {e}")
        raise