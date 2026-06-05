import logging
from ...agents.crew import weather_crew

logger = logging.getLogger(__name__)


def get_weather_forecast(location: str) -> dict:
    logger.info(f"Received location: {location}")
    input_data = {
        "location": location
    }
    logger.debug(f"Input data for weather_crew: {input_data}")
    try:
        result = weather_crew.kickoff(input_data)
        result_dict = result.to_dict()
        logger.info(f"Result from weather_crew: {result_dict}")
        return result_dict
    except ValueError as e:
        logger.warning(f"Invalid location: {str(e)}")
        raise
    