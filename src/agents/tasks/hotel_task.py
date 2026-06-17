from crewai import Task
from ..agent.hotel_agent import hotel_agents
from pydantic import BaseModel

class HotelOutput(BaseModel):
    hotels: list
    advice: str

hotel_tasks = Task(
    agent=hotel_agents,
    name="Hotel Recommendation Task",
    description="""Provide hotel recommendations for a specified location {location}.
                Instructions:
                - Use the hotel_finder tool to retrieve available hotel options for the specified location.
                - Analyze the retrieved data to provide a clear and concise summary of the available hotels, including their rates, popularity, and user ratings.
                - Provide detailed advice and recommendations for the user on which hotels to consider based on their preferences and the available options.
                -Provide also a ranking of the hotels based on popularity, price and user ratings, and make an estimated budget calculation for specific hotels.
                """,

    expected_output="""
    A structured JSON object with the following fields:
    - hotels: A list of dictionaries containing information about the available hotels, including their rates, popularity, address and user ratings.
    - advice: A string providing advice and recommendations based on the available hotel options.
    """,
    output_pydantic=HotelOutput
)
