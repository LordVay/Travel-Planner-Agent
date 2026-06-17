import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from crewai.tools import tool
from pydantic import BaseModel
from src.agents.config.api import AgentSettings
import requests

agent = AgentSettings()


class RestaurantInfo(BaseModel):
    name: str
    address: str
    rating: float
    price_level: int
    status: str


#@tool("Restaurant Finder Tool")
def restaurant_finder(city: str) -> list[dict]:
    """Find top-rated restaurants in a specified city for vacation dining."""
    api_key = agent.MAPS_API
    base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"

    params = {
        'query': f'restaurants in {city}',
        'type': 'restaurant',
        'key': api_key
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        res = response.json()

        if res.get("status") != "OK":
            raise ValueError(f"Could not find restaurants in '{city}'. API status: {res.get('status')}")

        restaurants = []
        for place in res.get("results", [])[:5]:
            restaurant = RestaurantInfo(
                name=place.get("name", "Unknown"),
                address=place.get("formatted_address", "No address available"),
                rating=place.get("rating", 0.0),
                price_level=place.get("price_level", 0),
                status="Open" if place.get("opening_hours", {}).get("open_now") else "Closed/Unknown"
            )
            restaurants.append(restaurant.model_dump())

        return restaurants
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Error connecting to Google Maps API: {str(e)}")
    