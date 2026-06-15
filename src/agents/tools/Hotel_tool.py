from crewai.tools import tool
from pydantic import BaseModel
import requests

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from src.agents.config.api import AgentSettings

agent = AgentSettings()


class HotelInfo(BaseModel):
    name: str
    address: str
    rating: float
    price_level: int
    status: str


#@tool("Hotel Finder Tool")
def hotel_finder(city: str) -> list[dict]:
    """Find top-rated hotels in a specified city for vacation stays."""
    api_key = agent.MAPS_API
    base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"

    params = {
        'query': f'hotels in {city}',
        'type': 'lodging',
        'key': api_key
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        res = response.json()

        if res.get("status") != "OK":
            raise ValueError(f"Could not find hotels in '{city}'. API status: {res.get('status')}")

        hotels = []
        for place in res.get("results", [])[:10]:
            hotel = HotelInfo(
                name=place.get("name", "Unknown"),
                address=place.get("formatted_address", "No address available"),
                rating=place.get("rating", 0.0),
                price_level=place.get("price_level", 0),
                status="Open" if place.get("opening_hours", {}).get("open_now") else "Closed/Unknown"
            )
            hotels.append(hotel.model_dump())

        return hotels
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Error connecting to Google Maps API: {str(e)}")

print(hotel_finder("Vigan"))