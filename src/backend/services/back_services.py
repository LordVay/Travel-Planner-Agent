# Service layer that bridges the FastAPI routes with the CrewAI agent system.
# Each function validates input, logs the request, and delegates to the appropriate crew.

import logging

from ...agents.crew import weather_crew
from ...agents.crew import attraction_crew
from ...agents.crew import hotel_crew
from ...agents.crew import restaurant_crew
from ...agents.crew import itenerary_crew
from ...agents.crew import budget_crew
from ...agents.crew import travel_planner_crew

logger = logging.getLogger("travelagent")


def _parse_string_values(data: dict) -> dict:
    """Parse string values that look like JSON lists/dicts back into Python objects."""
    import ast
    parsed = {}
    for key, val in data.items():
        if isinstance(val, str) and val.strip().startswith(("[", "{")):
            try:
                parsed[key] = ast.literal_eval(val)
            except (ValueError, SyntaxError):
                try:
                    import json
                    parsed[key] = json.loads(val)
                except (ValueError, json.JSONDecodeError):
                    parsed[key] = val
        elif isinstance(val, dict):
            parsed[key] = _parse_string_values(val)
        else:
            parsed[key] = val
    return parsed


def get_weather_forecast(location: str) -> dict:
    input_data = {"location": location}
    try:
        logger.info(f"Fetching weather forecast for: {location}")
        result = weather_crew.kickoff(input_data)
        data = result.to_dict()
        return _parse_string_values(data)
    except ValueError as e:
        logger.warning(f"Invalid location: {e}")
        raise


def get_attraction_guide(
    location: str,
    days: int,
    group_size: int,
    interests: str,
    intensity: str,
    events: str,
) -> dict:
    input_data = {
        "location": location,
        "days": days,
        "group_size": group_size,
        "interests": interests,
        "intensity": intensity,
        "events": events,
    }
    try:
        logger.info(f"Fetching attractions for: {location} ({group_size} travelers, {days} days)")
        result = attraction_crew.kickoff(input_data)
        return _parse_string_values(result.to_dict())
    except ValueError as e:
        logger.warning(f"Invalid input: {e}")
        raise


def get_itenerary(
    location: str,
    days: int,
    group_size: int,
    total_budget: str,
    interests: str,
    intensity: str,
    events: str,
    schedule_style: str,
) -> dict:
    input_data = {
        "location": location,
        "days": days,
        "group_size": group_size,
        "total_budget": total_budget,
        "interests": interests,
        "intensity": intensity,
        "events": events,
        "schedule_style": schedule_style,
    }
    try:
        logger.info(f"Generating {days}-day itinerary for: {location} ({group_size} travelers)")
        result = itenerary_crew.kickoff(input_data)
        return _parse_string_values(result.to_dict())
    except ValueError as e:
        logger.warning(f"Invalid input: {e}")
        raise


def get_hotel_recommendation(
    location: str,
    days: int,
    group_size: int,
    total_budget: str,
    hotel_preference: str,
) -> dict:
    input_data = {
        "location": location,
        "days": days,
        "group_size": group_size,
        "total_budget": total_budget,
        "hotel_preference": hotel_preference,
    }
    try:
        logger.info(f"Finding hotels in: {location} ({group_size} travelers, budget: {total_budget})")
        result = hotel_crew.kickoff(input_data)
        return _parse_string_values(result.to_dict())
    except ValueError as e:
        logger.warning(f"Invalid input: {e}")
        raise


def get_restaurant_recommendation(
    location: str,
    days: int,
    group_size: int,
    restaurant_preference: str,
    dietary_restrictions: str,
    meal_budget_per_day: str,
) -> dict:
    input_data = {
        "location": location,
        "days": days,
        "group_size": group_size,
        "restaurant_preference": restaurant_preference,
        "dietary_restrictions": dietary_restrictions,
        "meal_budget_per_day": meal_budget_per_day,
    }
    try:
        logger.info(f"Finding restaurants in: {location} ({group_size} travelers, cuisine: {restaurant_preference})")
        result = restaurant_crew.kickoff(input_data)
        return _parse_string_values(result.to_dict())
    except ValueError as e:
        logger.warning(f"Invalid input: {e}")
        raise


def get_budget_analysis(
    location: str,
    days: int,
    group_size: int,
    total_budget: str,
    interests: str,
    intensity: str,
    events: str,
    schedule_style: str,
    hotel_preference: str,
    restaurant_preference: str,
    dietary_restrictions: str,
    meal_budget_per_day: str,
) -> dict:
    input_data = {
        "location": location,
        "days": days,
        "group_size": group_size,
        "total_budget": total_budget,
        "interests": interests,
        "intensity": intensity,
        "events": events,
        "schedule_style": schedule_style,
        "hotel_preference": hotel_preference,
        "restaurant_preference": restaurant_preference,
        "dietary_restrictions": dietary_restrictions,
        "meal_budget_per_day": meal_budget_per_day,
    }
    try:
        logger.info(f"Generating budget analysis for: {location} ({group_size} travelers, {days} days, budget: {total_budget})")
        result = budget_crew.kickoff(input_data)
        return _parse_string_values(result.to_dict())
    except ValueError as e:
        logger.warning(f"Invalid input: {e}")
        raise


def get_travel_plan(
    location: str,
    days: int,
    group_size: int,
    total_budget: str,
    restaurant_preference: str,
    dietary_restrictions: str,
    meal_budget_per_day: str,
    hotel_preference: str,
    interests: str,
    intensity: str,
    events: str,
    schedule_style: str,
) -> dict:
    input_data = {
        "location": location,
        "days": days,
        "group_size": group_size,
        "total_budget": total_budget,
        "restaurant_preference": restaurant_preference,
        "dietary_restrictions": dietary_restrictions,
        "meal_budget_per_day": meal_budget_per_day,
        "hotel_preference": hotel_preference,
        "interests": interests,
        "intensity": intensity,
        "events": events,
        "schedule_style": schedule_style,
    }
    try:
        logger.info(f"Generating full travel plan for: {location} ({group_size} travelers, {days} days)")
        result = travel_planner_crew.kickoff(input_data)
        return _parse_string_values(result.to_dict())
    except ValueError as e:
        logger.warning(f"Invalid input: {e}")
        raise
