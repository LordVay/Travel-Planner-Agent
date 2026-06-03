from crewai import Task
import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from agent.weather_agent import weather_agents
from pydantic import BaseModel

class WeatherOutput(BaseModel):
    current_weather: dict
    forecast: dict
    advice: str

weather_tasks = Task(
    agent=weather_agents,
    name="Weather Forecasting Task",
    description="""Provide the current weather conditions and a 5-day forecast for this specified location {location}.
                Instructions:
                - Use the get_weather tool to retrieve current weather conditions for the specified location.
                - Use the get_forecast tool to retrieve a 5-day weather forecast for the specified
                - Analyze the retrieved data to provide a clear and concise summary of the current weather and the forecast, including any significant weather events or changes in conditions.
                - If the weather conditions indicate potential risks (e.g., storms, extreme temperatures), provide advice on how to prepare and stay safe.
                - Provide a detailed advice and recommendations for the user based on the weather conditions, such as what to wear, whether to carry an umbrella, or if any outdoor activities should be reconsidered.
                """,

    expected_output="""
    A structured JSON object with the following fields:
    - current_weather: A dictionary containing the current weather conditions.
    - forecast: A dictionary containing the 5-day weather forecast.
    - advice: A string providing advice and recommendations based on the weather conditions.
    """,
    output_pydantic=WeatherOutput
)
