from crewai.tools import tool
from pydantic import BaseModel
from ..config.api import AgentSettings
import requests

agent = AgentSettings()
agent.WEATHER_API

class WeatherInfo(BaseModel):
    location : str
    temperature : float
    description : str

class ForecastInfo(BaseModel):
    Day1 : dict
    Day2 : dict
    Day3 : dict
    Day4 : dict
    Day5 : dict

@tool("Current Weather Tool")
def weather_agent(city : str) -> WeatherInfo:
    """Get current weather information for a specified city."""
    api_key = agent.WEATHER_API
    base_url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        res = response.json()
        
        if res.get("cod") != 200:
            raise ValueError(f"City '{city}' not found. Please check the city name and try again.")
        
        return WeatherInfo(
            location=res["name"],
            description=res["weather"][0]["description"].capitalize(),
            temperature=res["main"]["temp"]
        )
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Error connecting to weather API: {str(e)}")
    except KeyError as e:
        raise ValueError(f"Invalid response format from weather API. Missing field: {str(e)}")
    except ValueError as e:
        raise e

@tool("5-Day Forecast Tool")
def forecast_agent(city : str) -> ForecastInfo:
    """Get 5-day weather forecast for a specified city."""
    api_key = agent.WEATHER_API
    base_url = "https://api.openweathermap.org/data/2.5/forecast"

    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        res = response.json()
        
        if res.get("cod") != "200":
            raise ValueError(f"City '{city}' not found. Please check the city name and try again.")
        
        forecast = []

        for i in range(0, len(res["list"]), 8):
            location = res["city"]["name"]
            description = res["list"][i]["weather"][0]["description"]
            temperature = res["list"][i]["main"]["temp"]
            cast = {
                "location" : location,
                "description": description,
                "temperature": temperature
            }
            forecast.append(cast)

        if len(forecast) < 5:
            raise ValueError(f"Insufficient forecast data for '{city}'. Expected at least 5 days of data.")

        return ForecastInfo(
            Day1=forecast[0],
            Day2=forecast[1],
            Day3=forecast[2],
            Day4=forecast[3],
            Day5=forecast[4]
        )
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Error connecting to weather API: {str(e)}")
    except KeyError as e:
        raise ValueError(f"Invalid response format from weather API. Missing field: {str(e)}")
    except ValueError as e:
        raise e

