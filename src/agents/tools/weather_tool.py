import os,sys
from crewai.tools import tool
from pydantic import BaseModel
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config.api import AgentSettings
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

@tool
def weather_agent(city : str) -> WeatherInfo:
    api_key = agent.WEATHER_API
    base_url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }

    res = requests.get(base_url, params=params).json()

    return WeatherInfo(
        location=res["name"],
        description=res["weather"][0]["description"].capitalize(),
        temperature=res["main"]["temp"]
    )

@tool
def forecast_agent(city : str) -> WeatherInfo:
    api_key = agent.WEATHER_API
    base_url = "https://api.openweathermap.org/data/2.5/forecast"

    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }

    res = requests.get(base_url, params=params).json()

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

   
    return ForecastInfo(
        Day1=forecast[0],
        Day2=forecast[1],
        Day3=forecast[2],
        Day4=forecast[3],
        Day5=forecast[4]
    )
    

print(forecast_agent("Manila"))

