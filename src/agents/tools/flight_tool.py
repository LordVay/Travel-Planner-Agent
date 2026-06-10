from crewai.tools import tool
from pydantic import BaseModel
import requests

try:
    # Package execution: python -m src.agents.tools.flight_tool
    from ..config.api import AgentSettings
except ImportError:
    # Direct script execution: python src/agents/tools/flight_tool.py
    from src.agents.config.api import AgentSettings

agent = AgentSettings()
agent.FLIGHT_API

class FlightInfo(BaseModel):
    airline : str
    arrival : str
    departure : str
    city: str

# @tool("Flight Tool")
def flight_agent(date: str, code: str) -> FlightInfo:
    """Get flight information for a given city."""
    api_key = agent.FLIGHT_API
    base_url = "https://api.aviationstack.com/v1/flightsFuture"

    params = {
        'access_key': api_key,
        'iataCode': code,
        'date': date,
        'type': 'departure',
        'limit': 3
    }

    try:
        response = requests.get(base_url, params=params, timeout=20)
        res = response.json()

        if not response.ok:
            api_error = res.get("error", {}) if isinstance(res, dict) else {}
            api_message = api_error.get("message") or response.text
            raise ValueError(f"Flight API request failed ({response.status_code}): {api_message}")

        data = res.get("data", []) if isinstance(res, dict) else []
        if not data:
            raise ValueError("No flights found for the provided date and IATA code.")

        print(res)

        
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Error connecting to flight API: {str(e)}")
    except KeyError as e:
        raise ValueError(f"Invalid response format from flight   API. Missing field: {str(e)}")
    except ValueError as e:
        raise e

if __name__ == "__main__":
    flight_agent("2026-06-12", "MNL")