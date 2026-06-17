from crewai import Task
from ..agent.restaurant_agent import restaurant_agents
from pydantic import BaseModel

class RestaurantOutput(BaseModel):
    restaurants: list
    advice: str

restaurant_tasks = Task(
    agent=restaurant_agents,
    name="Restaurant Recommendation Task",
    description="""Provide restaurant recommendations for a specified location {location}.
                Instructions:
                - Use the restaurant_finder tool to retrieve available restaurant options for the specified location.
                - Analyze the retrieved data to provide a clear and concise summary of the available restaurants, including their rates, popularity, and user ratings.
                - Provide detailed advice and recommendations for the user on which restaurants to consider based on their preferences and the available options.
                -Provide also a ranking of the restaurants based on popularity, price and user ratings, and make an estimated budget calculation for specific restaurants.
                """,

    expected_output="""
    A structured JSON object with the following fields:
    - restaurants: A list of dictionaries containing information about the available restaurants, including their rates, popularity, address and user ratings.
    - advice: A string providing advice and recommendations based on the available restaurant options.
    """,
    output_pydantic=RestaurantOutput
)
